import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chromadb
from agent.embedder import embed_texts

# Persistent ChromaDB stored in project folder
CHROMA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "chroma_db"
)

def get_collection():
    """Get or create the ChromaDB collection."""
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(
        name="research_papers",
        metadata={"hnsw:space": "cosine"}
    )
    return collection


def store_papers(papers: list):
    """Embed and store papers in ChromaDB."""
    collection = get_collection()

    # Filter out papers already stored
    new_papers = []
    for p in papers:
        try:
            collection.get(ids=[p["arxiv_id"]])
        except:
            new_papers.append(p)

    if not new_papers:
        print("  All papers already in vector store.")
        return

    print(f"  Storing {len(new_papers)} new papers in ChromaDB...")

    # Embed abstracts using IBM Slate
    texts    = [p["abstract"] for p in new_papers]
    vectors  = embed_texts(texts)

    # Store in ChromaDB with metadata
    collection.add(
        ids        = [p["arxiv_id"] for p in new_papers],
        embeddings = vectors,
        documents  = [p["abstract"] for p in new_papers],
        metadatas  = [{
            "title":   p["title"],
            "authors": ", ".join(p["authors"][:3]),
            "year":    str(p["year"]),
            "url":     p["url"]
        } for p in new_papers]
    )
    print(f"  Stored successfully. Total in DB: {collection.count()}")


def semantic_search(query: str, n_results: int = 5) -> list:
    """Search papers by meaning using vector similarity."""
    collection = get_collection()

    if collection.count() == 0:
        print("  Vector store is empty.")
        return []

    print(f"  Semantic search across {collection.count()} stored papers...")

    # Embed the query
    query_vector = embed_texts([query])[0]

    # Search ChromaDB
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=min(n_results, collection.count())
    )

    # Format results
    papers = []
    for i in range(len(results["ids"][0])):
        meta = results["metadatas"][0][i]
        papers.append({
            "title":     meta["title"],
            "authors":   meta["authors"].split(", "),
            "abstract":  results["documents"][0][i],
            "url":       meta["url"],
            "year":      int(meta["year"]),
            "arxiv_id":  results["ids"][0][i],
            "similarity": round(1 - results["distances"][0][i], 3)
        })

    return papers


def get_store_stats() -> dict:
    """Return stats about the vector store."""
    collection = get_collection()
    return {
        "total_papers": collection.count(),
        "db_path": CHROMA_PATH
    }


if __name__ == "__main__":
    stats = get_store_stats()
    print(f"Vector store has {stats['total_papers']} papers")