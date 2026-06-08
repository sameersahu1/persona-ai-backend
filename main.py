print("RAILWAY VERSION 999")
import os
import json
from pathlib import Path
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from tavily import TavilyClient
from groq import Groq
from duckduckgo_search import DDGS
import wikipediaapi

# Force Environment Setup
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="Persona Intelligence API (Groq Powered)")

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class SearchRequest(BaseModel):
    query: str

class ProfileSchema(BaseModel):
    status: str = Field(description="Must be 'success' or 'not_found'")
    confidence_score: int = Field(description="A calculated percentage from 0 to 100 based on source reliability.")
    summary: Optional[str] = Field(None, description="A comprehensive 2-paragraph overview summary.")
    insights: List[str] = Field(default=[], description="Bullet points detailing achievements.")
    sources: List[str] = Field(default=[], description="Verified URLs directly extracted.")

def gather_premium_intelligence(target_name: str, entity_type: str = "all"):
    aggregated_context = []
    
    # 1. DuckDuckGo Free Search Extraction
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text(f"{target_name} biography professional career", max_results=2)]
            for r in results:
                aggregated_context.append({"url": r['href'], "content": r['body']})
    except Exception as e:
        print(f"DDG Free Engine Error: {e}")

    # 2. Wikipedia API Free Extraction
    if entity_type in ["all", "person"]:
        try:
            wiki = wikipediaapi.Wikipedia(user_agent="PersonaIntelBot/1.0 (contact@yourdomain.com)", language="en")
            page = wiki.page(target_name)
            if page.exists():
                aggregated_context.append({"url": page.fullurl, "content": page.summary[:1200]})
        except Exception as e:
            print(f"Wikipedia API Error: {e}")

    return aggregated_context

def fetch_web_context(query: str) -> list:
    try:
        optimized_query = f"{query} professional background career biography news"
        response = tavily_client.search(query=optimized_query, search_depth="basic", max_results=4)
        return [{"url": res["url"], "content": res["content"]} for res in response.get("results", [])]
    except Exception as e:
        print(f"Tavily Search API Error: {e}")
        return []

@app.post("/api/profile", response_model=ProfileSchema)
def generate_intelligence_profile(request: SearchRequest):
    cleaned_query = request.query.strip()
    if not cleaned_query:
        raise HTTPException(status_code=400, detail="Search query cannot be empty.")

    # Gather data from all available data sources in parallel
    tavily_results = fetch_web_context(cleaned_query)
    premium_free_results = gather_premium_intelligence(cleaned_query)
    
    # Merge context objects into a single baseline array
    combined_context = tavily_results + premium_free_results

    if not combined_context:
        return ProfileSchema(
            status="not_found",
            confidence_score=0,
            summary=f"No public records found for '{cleaned_query}'.",
            insights=[],
            sources=[]
        )

    system_instruction = (
        "You are Persona, an advanced corporate intelligence system.\n"
        "Analyze the provided text context and output a profile structured in valid JSON matching this layout:\n"
        "{\n"
        '  "status": "success" or "not_found",\n'
        '  "confidence_score": 85,\n'
        '  "summary": "A comprehensive 2-paragraph profile overview text.",\n'
        '  "insights": ["Insight 1", "Insight 2"],\n'
        '  "sources": ["url1", "url2"]\n'
        "}\n\n"
        "CRITICAL RULES FOR VALUES:\n"
        "1. PURE PLAIN TEXT ONLY: The 'summary' and 'insights' fields MUST contain ONLY raw text sentences. "
        "Do NOT include any HTML formatting tags, markdown styles, or backticks inside these strings.\n"
        "2. Calculate 'confidence_score' as an integer from 0 to 100 based on resource credentials and stability.\n"
        "3. Rely ONLY on explicitly stated facts within the context. Never guess."
    )
    
    user_input = f"Target Entity: {cleaned_query}\n\nWeb Search Snippets:\n{json.dumps(combined_context)}"

    try:
        completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": "Reply with exactly: Hello"}
            ]
        )

        return ProfileSchema(
            status="success",
            confidence_score=100,
            summary=completion.choices[0].message.content,
            insights=["Groq connection successful"],
            sources=[]
        )

    except Exception as e:
        import traceback

        print("===== ERROR START =====")
        traceback.print_exc()
        print("ERROR:", repr(e))
        print("===== ERROR END =====")

        return ProfileSchema(
            status="error",
            confidence_score=0,
            summary=repr(e),
            insights=[],
            sources=[]
        )