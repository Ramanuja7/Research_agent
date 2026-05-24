import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import Embeddings

load_dotenv()

credentials = Credentials(
    url=os.getenv("WATSONX_URL"),
    api_key=os.getenv("WATSONX_APIKEY")
)

embedding_model = Embeddings(
    model_id="ibm/slate-125m-english-rtrvr-v2",
    credentials=credentials,
    project_id=os.getenv("WATSONX_PROJECT_ID")
)

def embed_texts(texts: list) -> list:
    """Convert list of texts to vectors using IBM Slate."""
    print(f"  Embedding {len(texts)} texts with IBM Slate...")
    response = embedding_model.embed_documents(texts=texts)
    return response


if __name__ == "__main__":
    test = embed_texts(["machine learning for medical imaging"])
    print(f"Vector dimension: {len(test[0])}")
    print(f"First 5 values: {test[0][:5]}")
    print("IBM Slate embeddings working!")