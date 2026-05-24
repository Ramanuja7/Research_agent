import streamlit as st
import sys, os, json
from datetime import datetime

# ── Fix Python path ──────────────────────────────────────────────────────────
current_file = os.path.abspath(__file__)
ui_folder    = os.path.dirname(current_file)
root_folder  = os.path.dirname(ui_folder)
sys.path.insert(0, root_folder)

from agent.agent import run_agent
from agent.search_tool import format_citation_apa

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.stApp { background: #0a0a0f; color: #e8e6f0; }

[data-testid="stSidebar"] {
    background: #0f0f1a;
    border-right: 1px solid #1e1e35;
}

.hero-title {
    font-family: 'DM Serif Display', serif;
    font-size: 3rem;
    line-height: 1.1;
    color: #ffffff;
    margin-bottom: 0.25rem;
}
.hero-title span { color: #7c6ff7; font-style: italic; }

.hero-sub {
    font-size: 1rem;
    color: #6b6880;
    font-weight: 300;
    letter-spacing: 0.02em;
    margin-bottom: 2.5rem;
}

.metric-row { display: flex; gap: 12px; margin-bottom: 2rem; }
.metric-card {
    background: #13131f;
    border: 1px solid #1e1e35;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    flex: 1;
}
.metric-label {
    font-size: 0.72rem;
    color: #6b6880;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.metric-value {
    font-family: 'DM Mono', monospace;
    font-size: 1.5rem;
    font-weight: 500;
    color: #7c6ff7;
}

.paper-card {
    background: #13131f;
    border: 1px solid #1e1e35;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}
.paper-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.05rem;
    color: #ffffff;
    margin-bottom: 0.4rem;
    line-height: 1.4;
}
.paper-meta {
    font-size: 0.78rem;
    color: #6b6880;
    font-family: 'DM Mono', monospace;
    margin-bottom: 0.5rem;
}
.paper-summary {
    font-size: 0.88rem;
    color: #a8a5be;
    line-height: 1.7;
    border-left: 2px solid #2a2a45;
    padding-left: 1rem;
    margin-top: 0.75rem;
}
.relevance-high {
    display: inline-block;
    background: #1a2e1a; color: #4ade80;
    border: 1px solid #2a4a2a;
    border-radius: 6px; font-size: 0.72rem;
    padding: 2px 8px; font-family: 'DM Mono', monospace; margin-left: 8px;
}
.relevance-medium {
    display: inline-block;
    background: #2a2a1a; color: #facc15;
    border: 1px solid #4a4a2a;
    border-radius: 6px; font-size: 0.72rem;
    padding: 2px 8px; font-family: 'DM Mono', monospace; margin-left: 8px;
}
.relevance-low {
    display: inline-block;
    background: #2a1a1a; color: #f87171;
    border: 1px solid #4a2a2a;
    border-radius: 6px; font-size: 0.72rem;
    padding: 2px 8px; font-family: 'DM Mono', monospace; margin-left: 8px;
}

.section-heading {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #7c6ff7;
    margin-bottom: 1rem;
    margin-top: 1.5rem;
}

.report-box {
    background: #0f0f1a;
    border: 1px solid #2a2a45;
    border-radius: 16px;
    padding: 2rem;
    margin-top: 1rem;
}

.citation-item {
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    color: #6b6880;
    padding: 0.6rem 0;
    border-bottom: 1px solid #1e1e35;
    line-height: 1.6;
}
.citation-num { color: #7c6ff7; margin-right: 8px; }

.history-item {
    background: #0f0f1a;
    border: 1px solid #1e1e35;
    border-radius: 10px;
    padding: 0.75rem 1rem;
    margin-bottom: 0.5rem;
    font-size: 0.85rem;
    color: #a8a5be;
}
.history-time {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #6b6880;
    margin-top: 2px;
}

.stButton > button {
    background: #7c6ff7 !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
    width: 100%;
}
.stButton > button:hover { opacity: 0.85 !important; }

.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #0f0f1a !important;
    border: 1px solid #2a2a45 !important;
    border-radius: 10px !important;
    color: #e8e6f0 !important;
}

div[data-testid="stExpander"] {
    background: #13131f;
    border: 1px solid #1e1e35 !important;
    border-radius: 12px !important;
}
hr { border-color: #1e1e35 !important; }
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "current_result" not in st.session_state:
    st.session_state.current_result = None


# ── Helper functions ──────────────────────────────────────────────────────────
def get_relevance_badge(summary_text):
    lower = summary_text.lower()
    idx = lower.find("relevance")
    if idx != -1:
        snippet = lower[idx:idx+40]
        if "high" in snippet:
            return '<span class="relevance-high">● High</span>'
        elif "medium" in snippet:
            return '<span class="relevance-medium">● Medium</span>'
        else:
            return '<span class="relevance-low">● Low</span>'
    return ""


def render_paper_card(entry, index):
    paper   = entry["paper"]
    summary = entry["summary"]
    authors = ", ".join(paper["authors"][:2])
    if len(paper["authors"]) > 2:
        authors += " et al."
    badge = get_relevance_badge(summary)
    st.markdown(f"""
    <div class="paper-card">
        <div class="paper-title">{index}. {paper['title']}</div>
        <div class="paper-meta">
            {authors} &nbsp;·&nbsp; {paper['year']} &nbsp;·&nbsp;
            arXiv:{paper.get('arxiv_id','N/A')} {badge}
        </div>
    </div>
    """, unsafe_allow_html=True)
    with st.expander("View AI Summary & PDF link"):
        st.markdown(
            f'<div class="paper-summary">{summary.replace(chr(10), "<br>")}</div>',
            unsafe_allow_html=True
        )
        st.markdown(f"[Open PDF ↗]({paper['url']})")


def generate_bibtex(papers):
    lines = []
    for p in papers:
        key = (p["authors"][0].split()[-1] if p["authors"] else "Unknown") + str(p["year"])
        lines.append(f"@article{{{key},")
        lines.append(f'  title  = {{{p["title"]}}},')
        lines.append(f'  author = {{{" and ".join(p["authors"])}}},')
        lines.append(f'  year   = {{{p["year"]}}},')
        lines.append(f'  url    = {{{p["url"]}}}')
        lines.append("}\n")
    return "\n".join(lines)


def save_outputs(result):
    os.makedirs("outputs", exist_ok=True)
    fname = f"outputs/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    return fname


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1rem 0 2rem">
        <div style="font-family:'DM Serif Display',serif;font-size:1.3rem;color:#fff">
            🔬 Research<span style="color:#7c6ff7;font-style:italic">Agent</span>
        </div>
        <div style="font-size:0.75rem;color:#6b6880;margin-top:4px;font-family:'DM Mono',monospace">
            Powered by IBM watsonx.ai
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-heading">Settings</div>', unsafe_allow_html=True)
    num_papers = st.slider("Papers to fetch", min_value=2, max_value=8, value=3)

    st.markdown("---")
    st.markdown('<div class="section-heading">Recent searches</div>', unsafe_allow_html=True)

    if st.session_state.history:
        for h in reversed(st.session_state.history[-5:]):
            st.markdown(f"""
            <div class="history-item">
                {h['query'][:38]}{'...' if len(h['query'])>38 else ''}
                <div class="history-time">{h['time']} &nbsp;·&nbsp; {h['papers']} papers</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(
            '<div style="color:#6b6880;font-size:0.82rem">No searches yet</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.75rem;color:#6b6880;line-height:2">
        <div>📡 &nbsp;arXiv API</div>
        <div>🤖 &nbsp;Llama 3.3 70B</div>
        <div>☁️ &nbsp;IBM watsonx.ai</div>
        <div>🌏 &nbsp;au-syd region</div>
    </div>
    """, unsafe_allow_html=True)


# ── Main layout ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-title">AI <span>Research</span> Agent</div>
<div class="hero-sub">Search · Summarise · Synthesise — powered by IBM watsonx.ai</div>
""", unsafe_allow_html=True)

# Search bar
query = st.text_input(
    "Research question",
    placeholder="e.g. transformer models for medical imaging diagnosis",
    label_visibility="collapsed"
)

col1, col2 = st.columns([4, 1])
with col1:
    run_btn = st.button("🔍  Run Research Agent", use_container_width=True)
with col2:
    clear_btn = st.button("Clear", use_container_width=True)

if clear_btn:
    st.session_state.current_result = None
    st.rerun()


# ── Agent execution ───────────────────────────────────────────────────────────
if run_btn:
    if not query.strip():
        st.warning("Please enter a research question first.")
    else:
        try:
            prog  = st.progress(0,  text="Starting...")
            stat  = st.empty()

            stat.info("🔍 Step 1/3 — Searching arXiv for papers...")
            prog.progress(10, text="Searching arXiv...")

            # Run the agent (all three steps happen inside)
            result = run_agent(query.strip(), num_papers=num_papers)

            prog.progress(70, text="Summarising papers...")
            stat.info("🤖 Step 2/3 — Summarising papers with Llama 3.3...")

            prog.progress(90, text="Generating report...")
            stat.info("📝 Step 3/3 — Writing research report...")

            save_outputs(result)

            st.session_state.current_result = result
            st.session_state.history.append({
                "query":  query.strip(),
                "time":   datetime.now().strftime("%H:%M"),
                "papers": result["papers_found"]
            })

            prog.progress(100, text="Done!")
            stat.empty()
            prog.empty()
            st.rerun()

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")
            st.code(str(e))


# ── Results display ───────────────────────────────────────────────────────────
if st.session_state.current_result:
    result = st.session_state.current_result

    # Metrics
    st.markdown(f"""
    <div class="metric-row">
        <div class="metric-card">
            <div class="metric-label">Papers found</div>
            <div class="metric-value">{result['papers_found']}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Semantic hits</div>
            <div class="metric-value">{result.get('semantic_hits', 0)}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Vector store</div>
            <div class="metric-value">{result.get('vector_store', 0)}</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">RAG enabled</div>
            <div class="metric-value" style="font-size:0.85rem;padding-top:8px;color:#4ade80">
                ✅ Active
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📄  Papers & Summaries", "📊  Research Report", "📥  Export"])

    # ── Tab 1: Papers ─────────────────────────────────────────────────────────
    with tab1:
        st.markdown('<div class="section-heading">Retrieved papers</div>',
                    unsafe_allow_html=True)
        for i, entry in enumerate(result["summaries"], 1):
            render_paper_card(entry, i)

    # ── Tab 2: Report ─────────────────────────────────────────────────────────
    with tab2:
        st.markdown('<div class="section-heading">AI-generated research report</div>',
                    unsafe_allow_html=True)
        st.markdown(
            f'<div style="font-size:0.82rem;color:#6b6880;font-family:DM Mono,monospace;'
            f'margin-bottom:1rem">Query: {result["query"]}</div>',
            unsafe_allow_html=True
        )
        st.markdown(result["report"])

        st.markdown("---")
        st.markdown('<div class="section-heading">References</div>', unsafe_allow_html=True)
        for i, c in enumerate(result["citations"], 1):
            st.markdown(
                f'<div class="citation-item"><span class="citation-num">[{i}]</span>{c}</div>',
                unsafe_allow_html=True
            )

    # ── Tab 3: Export ─────────────────────────────────────────────────────────
    with tab3:
        st.markdown('<div class="section-heading">Download your research</div>',
                    unsafe_allow_html=True)

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            md  = f"# Research Report\n\n**Query:** {result['query']}\n\n"
            md += f"**Generated:** {result['timestamp']}\n\n---\n\n"
            md += result["report"]
            md += "\n\n---\n\n## References\n\n"
            for i, c in enumerate(result["citations"], 1):
                md += f"[{i}] {c}\n\n"
            st.download_button(
                "⬇ Report (.md)",
                data=md,
                file_name=f"report_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown",
                use_container_width=True
            )

        with col_b:
            papers_list = [e["paper"] for e in result["summaries"]]
            bibtex      = generate_bibtex(papers_list)
            st.download_button(
                "⬇ Citations (.bib)",
                data=bibtex,
                file_name=f"citations_{datetime.now().strftime('%Y%m%d')}.bib",
                mime="text/plain",
                use_container_width=True
            )

        with col_c:
            json_str = json.dumps(result, indent=2, ensure_ascii=False)
            st.download_button(
                "⬇ Full data (.json)",
                data=json_str,
                file_name=f"research_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )

        st.markdown("---")
        with st.expander("View raw JSON"):
            st.json(result)

else:
    # Empty state
    st.markdown("""
    <div style="text-align:center;padding:5rem 2rem;color:#3a3a60">
        <div style="font-size:3.5rem;margin-bottom:1rem">🔬</div>
        <div style="font-family:'DM Serif Display',serif;font-size:1.5rem;
                    color:#2a2a45;margin-bottom:0.75rem">
            Enter a research question to begin
        </div>
        <div style="font-size:0.88rem;color:#3a3a60;max-width:420px;
                    margin:0 auto;line-height:1.8">
            The agent searches arXiv, summarises each paper using
            Llama 3.3 70B on IBM watsonx.ai, and generates a full
            research report — automatically.
        </div>
    </div>
    """, unsafe_allow_html=True)