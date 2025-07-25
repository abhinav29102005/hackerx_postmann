import pinecone
from pinecone import Pinecone
from dotenv import load_dotenv
import os

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"));
try:
    indexes = pc.list_indexes()
    print("✅ Pinecone connection successful!")
    print(f"Available indexes: {indexes.names()}")
except Exception as e:
    print(f"❌ Connection failed: {e}")