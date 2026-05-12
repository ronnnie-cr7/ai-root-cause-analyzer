import os
from dotenv import load_dotenv

load_dotenv()

# LLM Config
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.3-70b-versatile"

# ChromaDB Config
CHROMA_DB_PATH = "./data/chroma_db"
COLLECTION_NAME = "past_incidents"

# Paths
PAST_INCIDENTS_PATH = "./data/past_incidents.json"
SAMPLE_LOGS_PATH = "./data/sample_logs/"