import os
from dotenv import load_dotenv
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

load_dotenv()

credentials = Credentials(
    url=os.getenv("WATSONX_URL"),
    api_key=os.getenv("WATSONX_APIKEY")
)

model = ModelInference(
    model_id="meta-llama/llama-3-3-70b-instruct",
    credentials=credentials,
    project_id=os.getenv("WATSONX_PROJECT_ID"),
    params={
        "max_new_tokens": 1024,
        "temperature": 0.3,
        "repetition_penalty": 1.1
    }
)

def ask_model(prompt: str) -> str:
    response = model.generate_text(prompt=prompt)
    return response.strip()

if __name__ == "__main__":
    result = ask_model("In one sentence, what is machine learning?")
    print("Model says:", result)