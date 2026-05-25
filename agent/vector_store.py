import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import chromadb
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

from agent.embedder import embed_texts

CHROMA_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "chroma_db"
)

def get_collection():
    if not CHROMADB_AVAILABLE:
        raise ImportError("chromadb not installed")
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    return client.get_or_create_collection(
        name="research_papers",
        metadata={"hnsw:space": "cosine"}
    )

def store_papers(papers: list):
    if not CHROMADB_AVAILABLE:
        print("  ChromaDB not available - skipping vector store")
        return
    collection = get_collection()
    new_papers = []
    for p in papers:
        try:
            collection.get(ids=[p["arxiv_id"]])
        except:
            new_papers.append(p)
    if not new_papers:
        print("  All papers already in vector store.")
        return
    texts   = [p["abstract"] for p in new_papers]
    vectors = embed_texts(texts)
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

def semantic_search(query: str, n_results: int = 5) -> list:
    if not CHROMADB_AVAILABLE:
        return []
    collection = get_collection()
    if collection.count() == 0:
        return []
    query_vector = embed_texts([query])[0]
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=min(n_results, collection.count())
    )
    papers = []
    for i in range(len(results["ids"][0])):
        meta = results["metadatas"][0][i]
        papers.append({
            "title":      meta["title"],
            "authors":    meta["authors"].split(", "),
            "abstract":   results["documents"][0][i],
            "url":        meta["url"],
            "year":       int(meta["year"]),
            "arxiv_id":   results["ids"][0][i],
            "similarity": round(1 - results["distances"][0][i], 3)
        })
    return papers

def get_store_stats() -> dict:
    if not CHROMADB_AVAILABLE:
        return {"total_papers": 0, "db_path": "unavailable"}
    collection = get_collection()
    return {"total_papers": collection.count(), "db_path": CHROMA_PATH}