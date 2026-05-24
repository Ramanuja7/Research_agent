from agent.agent import run_agent

if __name__ == "__main__":
    # Change this to your research topic
    query = "transformer models for medical imaging diagnosis"

    result = run_agent(query, num_papers=3)

    print("\n" + "="*55)
    print("RESEARCH REPORT")
    print("="*55)
    print(result["report"])

    print("\n" + "="*55)
    print("REFERENCES")
    print("="*55)
    for i, c in enumerate(result["citations"], 1):
        print(f"[{i}] {c}")