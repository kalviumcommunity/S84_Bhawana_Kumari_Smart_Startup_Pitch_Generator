from huggingface_hub import login
from dotenv import load_dotenv
import os
from transformers import AutoTokenizer, AutoModel
import torch

# Load environment variables from .env
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
if HF_TOKEN is None:
    raise ValueError("HF_TOKEN not found. Please set it in your .env file or environment variables.")

login(token=HF_TOKEN)

# Use a sentence-transformer or similar embedding model
model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name, token=HF_TOKEN)
model = AutoModel.from_pretrained(model_name, token=HF_TOKEN)

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        # Mean pooling
        embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings.squeeze().numpy()

# Example usage
if __name__ == "__main__":
    sample_text = "AI-powered app that connects local farmers directly to restaurants."
    embedding = get_embedding(sample_text)
    print("Embedding shape:", embedding.shape)
    print("Embedding vector:", embedding)