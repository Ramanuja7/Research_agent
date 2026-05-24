import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agent.llm import ask_model

SUMMARY_PROMPT = """You are an expert research assistant.
Read the paper abstract below and produce a structured summary in EXACTLY this format:

Objective: (one sentence - what problem does this paper solve?)
Method: (1-2 sentences - what approach did they use?)
Key findings:
  - (finding 1)
  - (finding 2)
  - (finding 3)
Limitations: (one sentence - main weaknesses)
Relevance to "{query}": High / Medium / Low
Reason: (one sentence explaining the score)

Abstract:
{abstract}

Write only the structured summary. Nothing else."""

def summarise_paper(paper: dict, query: str) -> str:
    prompt = SUMMARY_PROMPT.format(
        abstract=paper["abstract"],
        query=query
    )
    return ask_model(prompt)

def summarise_all_papers(papers: list, query: str) -> list:
    enriched = []
    for i, paper in enumerate(papers):
        print(f"  Summarising {i+1}/{len(papers)}: {paper['title'][:55]}...")
        summary = summarise_paper(paper, query)
        enriched.append({
            "paper":   paper,
            "summary": summary
        })
    return enriched