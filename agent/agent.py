import os, json, sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.search_tool import search_papers, format_citation_apa
from agent.summariser import summarise_all_papers
from agent.vector_store import store_papers, semantic_search, get_store_stats
from agent.llm import ask_model

REPORT_PROMPT = """You are a senior research analyst.
Based on the following paper summaries about "{query}", write a professional research report:

## 1. Introduction
(2-3 sentences framing the topic and why it matters)

## 2. Key Themes Across Papers
(3 common themes or findings across all the papers)

## 3. Research Gaps
(What questions remain unanswered? What limitations appear repeatedly?)

## 4. Suggested Hypotheses
(2 original hypotheses for future research)

## 5. Conclusion
(1-2 sentences summarising the state of this field)

Paper summaries:
{summaries}

Write the full report now."""


def run_agent(query: str, num_papers: int = 5) -> dict:
    print(f"\n{'='*55}")
    print(f"  RAG Research Agent")
    print(f"  Query: {query}")
    print(f"{'='*55}\n")

    # ── Step 1: Fetch papers from arXiv ──────────────────────
    print("[1/5] Searching arXiv for papers...")
    papers = search_papers(query, max_results=num_papers)
    print(f"      Found {len(papers)} papers\n")

    # ── Step 2: Embed and store in ChromaDB ──────────────────
    print("[2/5] Embedding papers with IBM Slate...")
    store_papers(papers)
    stats = get_store_stats()
    print(f"      Vector store now has {stats['total_papers']} papers\n")

    # ── Step 3: Semantic search from vector store ─────────────
    print("[3/5] Semantic search across vector store...")
    semantic_results = semantic_search(query, n_results=num_papers)
    print(f"      Retrieved {len(semantic_results)} semantically similar papers\n")

    # Use semantic results if available, else fall back to arxiv results
    papers_to_use = semantic_results if semantic_results else papers

    # ── Step 4: Summarise each paper ─────────────────────────
    print("[4/5] Summarising papers with Llama 3.3 70B...")
    enriched = summarise_all_papers(papers_to_use, query)
    print("\n      All papers summarised\n")

    # ── Step 5: Generate research report ─────────────────────
    print("[5/5] Generating research report...")
    summary_text = "\n\n".join([
        f"Paper {i+1}: {e['paper']['title']}\n{e['summary']}"
        for i, e in enumerate(enriched)
    ])
    report = ask_model(
        REPORT_PROMPT.format(query=query, summaries=summary_text)
    )

    citations = [format_citation_apa(e["paper"]) for e in enriched]

    output = {
        "query":         query,
        "timestamp":     datetime.now().isoformat(),
        "papers_found":  len(papers),
        "semantic_hits": len(semantic_results),
        "vector_store":  stats["total_papers"],
        "summaries":     enriched,
        "report":        report,
        "citations":     citations,
        "rag_enabled":   True
    }

    os.makedirs("outputs", exist_ok=True)
    fname = f"outputs/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(fname, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n  Report saved to {fname}")
    return output