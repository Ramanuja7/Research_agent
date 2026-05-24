# 🔬 AI Research Agent

An autonomous AI-powered research assistant built with 
IBM watsonx.ai and RAG architecture.

## What it does
- Searches academic papers from arXiv automatically
- Summarises each paper using Llama 3.3 70B on IBM watsonx.ai
- Stores papers as vectors using IBM Slate 125M embeddings
- Performs semantic search using ChromaDB vector database
- Generates full research reports with citations
- Beautiful Streamlit web UI with export features

## Tech Stack
| Component | Technology |
|---|---|
| LLM | Llama 3.3 70B via IBM watsonx.ai |
| Embeddings | IBM Slate 125M |
| Vector DB | ChromaDB |
| Paper Search | arXiv API |
| UI | Streamlit |
| Architecture | RAG (Retrieval Augmented Generation) |

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/Ramanuja7/Research_agent.git
cd research-agent
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create your .env file
Create a `.env` file in the root folder:
### 5. Run the app
```bash
streamlit run ui/app.py
```

