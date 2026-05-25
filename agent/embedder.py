import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

try:
    from ibm_watsonx_ai import Credentials
    from ibm_watsonx_ai.foundation_models import Embeddings

    credentials = Credentials(
        url=os.getenv("WATSONX_URL"),
        api_key=os.getenv("WATSONX_APIKEY")
    )
    embedding_model = Embeddings(
        model_id="ibm/slate-125m-english-rtrvr-v2",
        credentials=credentials,
        project_id=os.getenv("WATSONX_PROJECT_ID")
    )
    EMBEDDINGS_AVAILABLE = True
except Exception:
    EMBEDDINGS_AVAILABLE = False

def embed_texts(texts: list) -> list:
    if not EMBEDDINGS_AVAILABLE:
        print("  Embeddings not available - skipping")
        return []
    print(f"  Embedding {len(texts)} texts with IBM Slate...")
    return embedding_model.embed_documents(texts=texts)