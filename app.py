import streamlit as st
import requests

# 1. Premium Page Setup
st.set_page_config(
    page_title="Persona Intelligence",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Advanced Premium CSS
st.markdown("""
<style>
    /* ===== FONT IMPORTS ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');
            
    /* Glowing Confidence Badge Component */
    .confidence-container {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 12px;
    }
    .confidence-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        font-weight: 600;
        padding: 4px 10px;
        border-radius: 6px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .conf-high {
        background: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid rgba(16, 185, 129, 0.3) !important;
        color: #34d399 !important;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.2);
    }
    .conf-med {
        background: rgba(245, 158, 11, 0.1) !important;
        border: 1px solid rgba(245, 158, 11, 0.3) !important;
        color: #fbbf24 !important;
        box-shadow: 0 0 15px rgba(245, 158, 11, 0.2);
    }
    .conf-low {
        background: rgba(239, 68, 68, 0.1) !important;
        border: 1px solid rgba(239, 68, 68, 0.3) !important;
        color: #f87171 !important;
        box-shadow: 0 0 15px rgba(239, 68, 68, 0.2);
    }
    /* ===== ROOT VARIABLES ===== */
    :root {
        --bg-primary: #030305;
        --bg-card: rgba(12, 12, 18, 0.6);
        --bg-card-hover: rgba(18, 18, 28, 0.8);
        --border-subtle: rgba(255, 255, 255, 0.04);
        --border-hover: rgba(255, 255, 255, 0.08);
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --text-muted: #64748b;
        --accent-purple: #a855f7;
        --accent-purple-dim: rgba(168, 85, 247, 0.15);
        --accent-cyan: #22d3ee;
        --accent-cyan-dim: rgba(34, 211, 238, 0.1);
        --accent-emerald: #10b981;
        --glow-purple: rgba(168, 85, 247, 0.25);
        --glass-bg: rgba(10, 10, 16, 0.5);
        --glass-border: rgba(255, 255, 255, 0.06);
        --radius-sm: 12px;
        --radius-md: 16px;
        --radius-lg: 24px;
        --radius-xl: 32px;
        --radius-full: 9999px;
    }
    
    /* ===== GLOBAL RESET ===== */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: var(--bg-primary) !important;
        color: var(--text-primary) !important;
        -webkit-font-smoothing: antialiased !important;
    }

    /* ===== ANIMATED BACKGROUND ===== */
    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background:
            radial-gradient(ellipse 80% 60% at 10% 15%, rgba(147, 51, 234, 0.07) 0%, transparent 50%),
            radial-gradient(ellipse 60% 80% at 85% 75%, rgba(6, 182, 212, 0.06) 0%, transparent 50%),
            radial-gradient(ellipse 50% 50% at 50% 50%, rgba(59, 130, 246, 0.03) 0%, transparent 60%);
        pointer-events: none;
        z-index: 0;
        animation: bgPulse 15s ease-in-out infinite alternate;
    }
    @keyframes bgPulse {
        0% { opacity: 0.7; }
        50% { opacity: 1; }
        100% { opacity: 0.8; }
    }

    /* ===== STREAMLIT OVERRIDES ===== */
    [data-testid="stHeader"] { background: transparent !important; }
    [data-testid="stToolbar"] { display: none !important; }
    [data-testid="stDecoration"] { display: none !important; }
    [data-testid="stSidebar"] { display: none !important; }
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }

    .block-container {
        padding: 1rem 1.5rem 4rem 1.5rem !important;
        max-width: 960px !important;
        position: relative;
        z-index: 1;
    }

    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: rgba(168, 85, 247, 0.3);
        border-radius: 10px;
    }

    /* ===== REMOVE ALL LINK UNDERLINES ===== */
    a, a:link, a:visited, a:hover, a:active,
    a:focus, a *, .nav-link, .source-chip,
    .source-url, .app-footer a {
        text-decoration: none !important;
        text-decoration-line: none !important;
        text-decoration-style: unset !important;
        text-underline-offset: unset !important;
        border-bottom: none !important;
        box-shadow: none !important;
        outline: none !important;
        -webkit-text-decoration: none !important;
    }

    /* ===== NAVBAR ===== */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 24px;
        background: rgba(8, 8, 14, 0.75);
        backdrop-filter: blur(40px) saturate(180%);
        -webkit-backdrop-filter: blur(40px) saturate(180%);
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-lg);
        margin-bottom: 2.5rem;
        position: relative;
        overflow: hidden;
        flex-wrap: wrap;
        gap: 8px;
    }
    .navbar::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(168, 85, 247, 0.3), rgba(34, 211, 238, 0.3), transparent);
    }
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        text-decoration: none !important;
        border-bottom: none !important;
        min-width: 0;
    }
    .nav-icon {
        width: 34px;
        height: 34px;
        background: linear-gradient(135deg, var(--accent-purple), var(--accent-cyan));
        border-radius: 9px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        box-shadow: 0 4px 15px var(--glow-purple);
        flex-shrink: 0;
    }
    .nav-title {
        font-weight: 700;
        font-size: 17px;
        background: linear-gradient(135deg, #ffffff 0%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.3px;
        white-space: nowrap;
    }
    .nav-tag {
        font-size: 9px;
        color: var(--text-muted);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        background: rgba(255,255,255,0.04);
        padding: 2px 8px;
        border-radius: var(--radius-full);
        border: 1px solid var(--border-subtle);
        white-space: nowrap;
    }
    .nav-links {
        display: flex;
        gap: 3px;
        align-items: center;
        flex-wrap: wrap;
    }
    .nav-link {
        color: var(--text-muted) !important;
        text-decoration: none !important;
        border-bottom: none !important;
        font-size: 12.5px;
        font-weight: 500;
        padding: 6px 14px;
        border-radius: var(--radius-full);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        white-space: nowrap;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }
    .nav-link:hover {
        color: var(--text-primary) !important;
        background: rgba(255, 255, 255, 0.05);
        text-decoration: none !important;
    }
    .nav-link.active {
        color: #ffffff !important;
        background: rgba(168, 85, 247, 0.12);
        border: 1px solid rgba(168, 85, 247, 0.2);
        text-decoration: none !important;
    }

    /* ===== HERO SECTION - FULLY CENTERED ===== */
    .hero {
        text-align: center;
        margin-bottom: 2rem;
        position: relative;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        width: 100%;
    }
    .hero-glow {
        position: absolute;
        top: -60px;
        left: 50%;
        transform: translateX(-50%);
        width: 350px;
        height: 180px;
        background: radial-gradient(ellipse, rgba(168, 85, 247, 0.12) 0%, transparent 70%);
        pointer-events: none;
        filter: blur(40px);
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.08), rgba(34, 211, 238, 0.06));
        border: 1px solid rgba(168, 85, 247, 0.15);
        padding: 5px 18px;
        border-radius: var(--radius-full);
        color: #c084fc;
        font-size: 10.5px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1.8rem;
    }
    @keyframes badgeGlow {
        0% { box-shadow: 0 0 15px rgba(168, 85, 247, 0.1); }
        100% { box-shadow: 0 0 25px rgba(168, 85, 247, 0.2); }
    }
    .hero-badge-dot {
        width: 6px;
        height: 6px;
        background: #a855f7;
        border-radius: 50%;
        animation: pulse 2s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(0.8); }
    }
    .hero h1 {
        font-size: clamp(26px, 5vw, 50px);
        font-weight: 800;
        letter-spacing: -1.5px;
        line-height: 1.15;
        margin: 0 auto 14px auto;
        color: #f8fafc;
        text-align: center;
        width: 100%;
    }
    .hero h1 .gradient-text {
        background: linear-gradient(135deg, #c084fc 0%, #38bdf8 50%, #22d3ee 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-size: 200% 200%;
        animation: gradientShift 6s ease-in-out infinite;
    }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* ===== HERO DESCRIPTION - FORCE CENTERED ===== */
    .hero-desc {
        font-size: clamp(13px, 1.8vw, 15.5px);
        color: var(--text-secondary);
        width: 100%;
        max-width: 540px;
        margin-left: auto !important;
        margin-right: auto !important;
        text-align: center !important;
        line-height: 1.7;
        font-weight: 400;
        display: block;
        padding: 0 1rem;
        box-sizing: border-box;
    }

    /* ===== SEARCH ALIGNMENT ===== */
    [data-testid="stHorizontalBlock"] {
        gap: 10px !important;
        align-items: stretch !important;
        flex-wrap: nowrap !important;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] {
        display: flex !important;
        flex-direction: column !important;
    }
    [data-testid="stHorizontalBlock"] > [data-testid="stVerticalBlockBorderWrapper"] > div {
        flex: 1 !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-end !important;
    }

    /* ===== SEARCH INPUT ===== */
    .stTextInput > div { height: 100% !important; }
    .stTextInput > div > div { height: 100% !important; }
    .stTextInput input {
        background: var(--glass-bg) !important;
        backdrop-filter: blur(30px) saturate(150%) !important;
        -webkit-backdrop-filter: blur(30px) saturate(150%) !important;
        border: 1px solid var(--glass-border) !important;
        border-radius: 16px !important;
        color: #ffffff !important;
        font-size: 14.5px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 400 !important;
        padding: 0 22px !important;
        height: 52px !important;
        box-sizing: border-box !important;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow:
            0 4px 24px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.03) !important;
        width: 100% !important;
    }
    .stTextInput input::placeholder {
        color: var(--text-muted) !important;
        font-weight: 400 !important;
    }
    .stTextInput input:focus {
        border-color: rgba(168, 85, 247, 0.5) !important;
        box-shadow:
            0 0 0 3px rgba(168, 85, 247, 0.08),
            0 4px 40px rgba(168, 85, 247, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.05) !important;
        outline: none !important;
    }
    .stTextInput label { display: none !important; }

    /* ===== SEARCH BUTTON ===== */
    .stButton > button {
        background: linear-gradient(135deg, #9333ea 0%, #7c3aed 50%, #6d28d9 100%) !important;
        border: none !important;
        color: white !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        font-size: 13.5px !important;
        height: 52px !important;
        padding: 0 28px !important;
        border-radius: 16px !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow:
            0 4px 20px rgba(147, 51, 234, 0.35),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        letter-spacing: 0.3px !important;
        white-space: nowrap !important;
        box-sizing: border-box !important;
        width: 100% !important;
        min-width: 120px !important;
        line-height: 52px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow:
            0 8px 30px rgba(147, 51, 234, 0.5),
            0 0 60px rgba(147, 51, 234, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
    }
    .stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* ===== REMOVE SPACING ===== */
    .stTextInput { margin-bottom: 0 !important; }
    .stButton { margin-top: 0 !important; margin-bottom: 0 !important; }
    [data-testid="stVerticalBlockBorderWrapper"] {
        padding: 0 !important;
        border: none !important;
    }
    [data-testid="stVerticalBlock"] { gap: 0 !important; }
    [data-testid="stElementContainer"] { margin: 0 !important; }

    /* ===== FILTER PILLS ===== */
    .filters {
        display: flex;
        justify-content: center;
        gap: 7px;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        flex-wrap: wrap;
        padding: 0 1rem;
    }
    .pill {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid var(--border-subtle);
        padding: 6px 16px;
        border-radius: var(--radius-full);
        font-size: 12px;
        font-weight: 500;
        color: var(--text-muted);
        cursor: pointer;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        user-select: none;
        white-space: nowrap;
    }
    .pill:hover {
        border-color: var(--border-hover);
        color: var(--text-secondary);
        background: rgba(255, 255, 255, 0.03);
        transform: translateY(-1px);
    }
    .pill.active {
        background: var(--accent-purple-dim);
        border-color: rgba(168, 85, 247, 0.35);
        color: #e9d5ff;
        box-shadow: 0 2px 12px rgba(168, 85, 247, 0.15);
    }
    .pill .pill-icon {
        margin-right: 4px;
        font-size: 11px;
    }

    /* ===== STATS ROW ===== */
    .stats-row {
        display: flex;
        justify-content: center;
        gap: 28px;
        margin: 2.2rem 0 0.5rem 0;
        padding: 0 1rem;
        flex-wrap: wrap;
    }
    .stat-item { text-align: center; }
    .stat-value {
        font-size: 20px;
        font-weight: 700;
        background: linear-gradient(135deg, #e2e8f0, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .stat-label {
        font-size: 10px;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 500;
        margin-top: 3px;
    }

    /* ===== SECTION DIVIDER ===== */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--border-subtle), transparent);
        margin: 2rem 0;
    }

    /* ===== RESULT CARDS ===== */
    .result-card {
        background: var(--bg-card);
        backdrop-filter: blur(40px) saturate(150%);
        -webkit-backdrop-filter: blur(40px) saturate(150%);
        border: 1px solid var(--glass-border);
        border-radius: var(--radius-lg);
        padding: 28px;
        margin-top: 20px;
        position: relative;
        overflow: hidden;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        animation: cardSlideIn 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
        opacity: 0;
        transform: translateY(20px);
    }
    .result-card:nth-child(1) { animation-delay: 0.1s; }
    .result-card:nth-child(2) { animation-delay: 0.25s; }
    .result-card:nth-child(3) { animation-delay: 0.4s; }
    @keyframes cardSlideIn {
        to { opacity: 1; transform: translateY(0); }
    }
    .result-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--glass-border), transparent);
    }
    .result-card:hover {
        border-color: var(--border-hover);
        background: var(--bg-card-hover);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
        transform: translateY(-2px);
    }
    .result-card.cyan-accent::after {
        content: ''; position: absolute; top: 0; left: 24px; width: 50px; height: 2px;
        background: linear-gradient(90deg, var(--accent-cyan), transparent);
    }
    .result-card.purple-accent::after {
        content: ''; position: absolute; top: 0; left: 24px; width: 50px; height: 2px;
        background: linear-gradient(90deg, var(--accent-purple), transparent);
    }
    .result-card.emerald-accent::after {
        content: ''; position: absolute; top: 0; left: 24px; width: 50px; height: 2px;
        background: linear-gradient(90deg, var(--accent-emerald), transparent);
    }

    /* ===== CARD HEADERS ===== */
    .card-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 18px;
    }
    .card-icon {
        width: 36px;
        height: 36px;
        border-radius: var(--radius-sm);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 15px;
        flex-shrink: 0;
    }
    .card-icon.cyan {
        background: var(--accent-cyan-dim);
        border: 1px solid rgba(34, 211, 238, 0.15);
        color: var(--accent-cyan);
    }
    .card-icon.purple {
        background: var(--accent-purple-dim);
        border: 1px solid rgba(168, 85, 247, 0.2);
        color: var(--accent-purple);
    }
    .card-icon.emerald {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.15);
        color: var(--accent-emerald);
    }
    .card-label { font-size: 15px; font-weight: 600; letter-spacing: -0.3px; }
    .card-label.cyan { color: var(--accent-cyan); }
    .card-label.purple { color: #c084fc; }
    .card-label.emerald { color: var(--accent-emerald); }
    .card-sublabel {
        font-size: 10.5px;
        color: var(--text-muted);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 2px;
    }
    .card-body {
        color: #cbd5e1;
        font-size: 14px;
        line-height: 1.75;
        font-weight: 380;
    }

    /* ===== INSIGHT LIST ===== */
    .insight-list { list-style: none; padding: 0; margin: 0; }
    .insight-item {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 12px 14px;
        margin-bottom: 4px;
        border-radius: var(--radius-md);
        transition: all 0.2s;
        color: #cbd5e1;
        font-size: 13.5px;
        line-height: 1.65;
        font-weight: 380;
    }
    .insight-item:hover { background: rgba(255, 255, 255, 0.02); }
    .insight-bullet {
        width: 22px;
        height: 22px;
        border-radius: 7px;
        background: var(--accent-purple-dim);
        border: 1px solid rgba(168, 85, 247, 0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        margin-top: 1px;
        font-size: 10px;
        color: #c084fc;
        font-weight: 700;
    }

    /* ===== SOURCE BADGES ===== */
    .sources-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
        gap: 8px;
        margin-top: 8px;
    }
    .source-chip {
        display: flex;
        align-items: center;
        gap: 10px;
        background: rgba(34, 211, 238, 0.04);
        border: 1px solid rgba(34, 211, 238, 0.1);
        padding: 11px 14px;
        border-radius: var(--radius-md);
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .source-chip:hover {
        background: rgba(34, 211, 238, 0.08);
        border-color: rgba(34, 211, 238, 0.3);
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(34, 211, 238, 0.1);
    }
    .source-favicon {
        width: 18px;
        height: 18px;
        border-radius: 4px;
        background: rgba(34, 211, 238, 0.1);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        font-size: 9px;
    }
    .source-url {
        color: var(--accent-cyan) !important;
        font-size: 12px;
        font-weight: 500;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        font-family: 'JetBrains Mono', monospace;
    }
    .source-arrow {
        color: var(--text-muted);
        font-size: 11px;
        margin-left: auto;
        flex-shrink: 0;
        transition: transform 0.2s;
    }
    .source-chip:hover .source-arrow {
        transform: translateX(3px);
        color: var(--accent-cyan);
    }

    /* ===== LOADING ===== */
    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 50px 20px;
        gap: 18px;
    }
    .loading-orb {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--accent-purple), var(--accent-cyan));
        animation: orbPulse 1.5s ease-in-out infinite;
        box-shadow: 0 0 40px var(--glow-purple);
    }
    @keyframes orbPulse {
        0%, 100% { transform: scale(1); opacity: 0.8; }
        50% { transform: scale(1.15); opacity: 1; }
    }
    .loading-text {
        color: var(--text-secondary);
        font-size: 13.5px;
        font-weight: 500;
        animation: textFade 2s ease-in-out infinite;
    }
    @keyframes textFade {
        0%, 100% { opacity: 0.6; }
        50% { opacity: 1; }
    }

    /* ===== ALERTS ===== */
    .alert-card {
        background: rgba(239, 68, 68, 0.06);
        border: 1px solid rgba(239, 68, 68, 0.15);
        border-radius: var(--radius-lg);
        padding: 22px 24px;
        margin-top: 20px;
        display: flex;
        align-items: flex-start;
        gap: 12px;
    }
    .alert-card.warning {
        background: rgba(245, 158, 11, 0.06);
        border-color: rgba(245, 158, 11, 0.15);
    }
    .alert-icon { font-size: 18px; flex-shrink: 0; margin-top: 1px; }
    .alert-text { color: #fca5a5; font-size: 13.5px; line-height: 1.6; }
    .alert-card.warning .alert-text { color: #fcd34d; }

    /* ===== FOOTER ===== */
    .app-footer {
        text-align: center;
        padding: 3rem 1rem 1rem 1rem;
        color: var(--text-muted);
        font-size: 11.5px;
    }
    .app-footer a {
        color: var(--accent-purple) !important;
    }

    /* ===== SPINNER OVERRIDE ===== */
    .stSpinner > div { display: none !important; }

    /* ===== RESPONSIVE - TABLET ===== */
    @media (max-width: 768px) {
        .block-container {
            padding: 0.75rem 0.75rem 3rem 0.75rem !important;
        }
        .navbar {
            padding: 10px 14px;
            border-radius: var(--radius-md);
            margin-bottom: 1.8rem;
            justify-content: center;
        }
        .nav-links { display: none !important; }
        .nav-tag { display: none !important; }
        .hero h1 {
            font-size: 26px !important;
            letter-spacing: -0.5px;
        }
        .hero-desc {
            font-size: 13px !important;
            padding: 0 0.5rem !important;
            max-width: 100% !important;
            margin-left: auto !important;
            margin-right: auto !important;
            text-align: center !important;
        }
        .hero-badge {
            font-size: 9.5px;
            padding: 4px 12px;
        }

        /* Search stacks on mobile */
        [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            gap: 8px !important;
        }
        .stTextInput input {
            height: 48px !important;
            font-size: 14px !important;
            border-radius: 14px !important;
            padding: 0 18px !important;
        }
        .stButton > button {
            height: 48px !important;
            border-radius: 14px !important;
            font-size: 13px !important;
            min-width: unset !important;
            width: 100% !important;
        }

        .result-card {
            padding: 20px 16px;
            border-radius: var(--radius-md);
            margin-top: 14px;
        }
        .filters {
            gap: 5px;
            justify-content: flex-start;
            overflow-x: auto;
            flex-wrap: nowrap;
            padding: 0 0.5rem 6px 0.5rem;
            -ms-overflow-style: none;
            scrollbar-width: none;
        }
        .filters::-webkit-scrollbar { display: none; }
        .sources-grid { grid-template-columns: 1fr; }
        .stats-row { gap: 16px; }
        .stat-value { font-size: 18px; }
        .stat-label { font-size: 9px; }
        .card-icon { width: 30px; height: 30px; font-size: 13px; }
        .card-label { font-size: 13.5px; }
        .card-sublabel { font-size: 9.5px; }
        .card-body { font-size: 13px; }
        .insight-item { font-size: 12.5px; padding: 10px 10px; gap: 10px; }
        .insight-bullet { width: 20px; height: 20px; font-size: 9px; border-radius: 6px; }
    }

    /* ===== RESPONSIVE - SMALL MOBILE ===== */
    @media (max-width: 480px) {
        .block-container {
            padding: 0.5rem 0.5rem 2.5rem 0.5rem !important;
        }
        .hero h1 { font-size: 22px !important; }
        .hero-desc {
            font-size: 12.5px !important;
            padding: 0 0.25rem !important;
            text-align: center !important;
        }
        .navbar { padding: 8px 12px; border-radius: 12px; margin-bottom: 1.5rem; }
        .nav-icon { width: 28px; height: 28px; font-size: 13px; border-radius: 7px; }
        .nav-title { font-size: 15px; }
        .result-card { padding: 16px 12px; margin-top: 12px; }
        .card-header { gap: 8px; margin-bottom: 14px; }
        .insight-item { padding: 8px 8px; font-size: 12px; }
        .source-chip { padding: 9px 10px; }
        .source-url { font-size: 11px; }
        .pill { padding: 5px 12px; font-size: 11px; }
        .stats-row { gap: 12px; margin: 1.8rem 0 0.3rem 0; }
        .stat-value { font-size: 16px; }
        .hero-glow { width: 250px; height: 120px; }
    }

    /* ===== LARGE DESKTOP ===== */
    @media (min-width: 1200px) {
        .block-container { max-width: 900px !important; }
    }
</style>
""", unsafe_allow_html=True)


# 3. Navbar
st.markdown("""
<div class="navbar">
    <div class="nav-brand">
        <div class="nav-icon">✦</div>
        <div>
            <span class="nav-title">Persona</span>
            <span class="nav-tag">Intelligence</span>
        </div>
    </div>
    <div class="nav-links">
        <a href="#" class="nav-link active">⚡ Discover</a>
        <a href="#" class="nav-link">📁 Saved</a>
        <a href="#" class="nav-link">🔑 API</a>
        <a href="#" class="nav-link">⚙ Settings</a>
    </div>
</div>
""", unsafe_allow_html=True)


# 4. Hero Section - Fully Centered
st.markdown("""
<div class="hero">
    <div class="hero-glow"></div>
    <div class="hero-badge">
        <span class="hero-badge-dot"></span>
        AI-Powered Intelligence Engine
    </div>
    <h1>
        Discover who matters.<br>
        <span class="gradient-text">Understand them instantly.</span>
    </h1>
    <p class="hero-desc">
        Search founders, investors, professionals, and companies.
        Get AI-synthesized summaries, verified sources, and deep strategic insights — in seconds.
    </p>
</div>
""", unsafe_allow_html=True)


# 5. Search Bar & Button
col_search, col_btn = st.columns([5, 1])

with col_search:
    query_input = st.text_input(
        label="search",
        placeholder="Search people, companies, or topics...",
        label_visibility="collapsed",
        key="main_search"
    )

with col_btn:
    search_button = st.button("✦  Search", use_container_width=True, key="search_btn")


# 6. Filter Pills
st.markdown("""
<div class="filters">
    <div class="pill active"><span class="pill-icon">◎</span> All</div>
    <div class="pill"><span class="pill-icon">👤</span> Founders</div>
    <div class="pill"><span class="pill-icon">💰</span> Investors</div>
    <div class="pill"><span class="pill-icon">🏢</span> Companies</div>
    <div class="pill"><span class="pill-icon">🚀</span> Startups</div>
    <div class="pill"><span class="pill-icon">🎓</span> Academics</div>
    <div class="pill"><span class="pill-icon">🌐</span> Organizations</div>
</div>
""", unsafe_allow_html=True)


# 7. Stats Row
st.markdown("""
<div class="stats-row">
    <div class="stat-item">
        <div class="stat-value">2.4M+</div>
        <div class="stat-label">Profiles Indexed</div>
    </div>
    <div class="stat-item">
        <div class="stat-value">150+</div>
        <div class="stat-label">Data Sources</div>
    </div>
    <div class="stat-item">
        <div class="stat-value">0.8s</div>
        <div class="stat-label">Avg. Response</div>
    </div>
    <div class="stat-item">
        <div class="stat-value">99.2%</div>
        <div class="stat-label">Accuracy Rate</div>
    </div>
</div>
""", unsafe_allow_html=True)


# 8. Search Logic
if search_button and query_input:
    loading_placeholder = st.empty()
    loading_placeholder.markdown("""
    <div class="loading-container">
        <div class="loading-orb"></div>
        <div class="loading-text">Synthesizing intelligence from multiple sources...</div>
    </div>
    """, unsafe_allow_html=True)

    try:
        backend_url = "http://127.0.0.1:8000/api/profile"
        response = requests.post(backend_url, json={"query": query_input}, timeout=45)
        loading_placeholder.empty()

        if response.status_code == 200:
            data = response.json()

            if data["status"] == "success":
                st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

                score = data.get("confidence_score", 85)
                
                if score >= 85:
                    status_class = "conf-high"
                    status_text = "High Reliability"
                elif score >= 60:
                    status_class = "conf-med"
                    status_text = "Moderate Reliability"
                else:
                    status_class = "conf-low"
                    status_text = "Low Reliability"

                # Card A - Executive Summary (Flush-Left String Placement)
                st.markdown(f"""
<div class="result-card cyan-accent">
    <div class="card-header" style="margin-bottom: 10px;">
        <div class="card-icon cyan">📋</div>
        <div>
            <div class="card-label cyan">Executive Intelligence Briefing</div>
            <div class="card-sublabel">AI-synthesized overview</div>
        </div>
    </div>
    <div class="confidence-container">
        <span class="confidence-badge {status_class}">● {status_text}</span>
        <span style="color: #64748b; font-size: 12px; font-family: 'JetBrains Mono', monospace;">Score: {score}%</span>
    </div>
    <div class="card-body" style="margin-top: 10px;">
        {data['summary']}
    </div>
</div>
""", unsafe_allow_html=True)

                # Card B - Insights
                insights_items = ""
                for i, insight in enumerate(data["insights"], 1):
                    insights_items += f"""
                    <li class="insight-item">
                        <div class="insight-bullet">{i}</div>
                        <span>{insight}</span>
                    </li>"""

                # Card B UI Injection (Flush-Left String Placement)
                st.markdown(f"""
<div class="result-card purple-accent">
    <div class="card-header">
        <div class="card-icon purple">⚡</div>
        <div>
            <div class="card-label purple">Strategic Profile Insights</div>
            <div class="card-sublabel">Key findings & analysis</div>
        </div>
    </div>
    <ul class="insight-list">{insights_items}</ul>
</div>
""", unsafe_allow_html=True)

                # Card C - Sources
                source_chips = ""
                for url in data["sources"]:
                    short_url = url.split("//")[-1][:32]
                    source_chips += f"""
                    <a href="{url}" target="_blank" class="source-chip" rel="noopener noreferrer">
                        <div class="source-favicon">🔗</div>
                        <span class="source-url">{short_url}</span>
                        <span class="source-arrow">→</span>
                    </a>"""

                # Card C UI Injection (Flush-Left String Placement)
                st.markdown(f"""
<div class="result-card emerald-accent">
    <div class="card-header">
        <div class="card-icon emerald">🛡️</div>
        <div>
            <div class="card-label emerald">Verified Citations & Sources</div>
            <div class="card-sublabel">{len(data['sources'])} references found</div>
        </div>
    </div>
    <div class="sources-grid">{source_chips}</div>
</div>
""", unsafe_allow_html=True)

            elif data["status"] == "not_found":
                st.markdown(f"""
                <div class="alert-card warning">
                    <span class="alert-icon">⚠️</span>
                    <span class="alert-text">{data['summary']}</span>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="alert-card">
                    <span class="alert-icon">❌</span>
                    <span class="alert-text">{data['summary']}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="alert-card">
                <span class="alert-icon">🔴</span>
                <span class="alert-text">Upstream error — HTTP <strong>{response.status_code}</strong>. Check your backend.</span>
            </div>
            """, unsafe_allow_html=True)

    except requests.exceptions.ConnectionError:
        loading_placeholder.empty()
        st.markdown("""
        <div class="alert-card">
            <span class="alert-icon">🔴</span>
            <span class="alert-text"><strong>Connection refused.</strong> FastAPI not reachable at
            <code style="color:#f87171;background:rgba(239,68,68,0.1);padding:2px 8px;border-radius:6px;font-family:'JetBrains Mono',monospace;font-size:11px;">localhost:8000</code>.
            Start your server first.</span>
        </div>
        """, unsafe_allow_html=True)

    except requests.exceptions.Timeout:
        loading_placeholder.empty()
        st.markdown("""
        <div class="alert-card warning">
            <span class="alert-icon">⏱️</span>
            <span class="alert-text"><strong>Timed out.</strong> Backend took too long. Try again.</span>
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        loading_placeholder.empty()
        st.markdown(f"""
        <div class="alert-card">
            <span class="alert-icon">💥</span>
            <span class="alert-text">Unexpected error:
            <code style="color:#f87171;background:rgba(239,68,68,0.1);padding:2px 8px;border-radius:6px;font-size:11px;">{str(e)}</code></span>
        </div>
        """, unsafe_allow_html=True)


# 9. Footer
st.markdown("""
<div class="app-footer">
    <div class="section-divider"></div>
    <p style="margin-top:1.5rem;">
        Built with ✦ by <a href="#">Persona Intelligence</a> ·
        Powered by advanced AI ·
        <span style="color:#475569;">v2.0</span>
    </p>
</div>
""", unsafe_allow_html=True)