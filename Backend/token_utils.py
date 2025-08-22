from huggingface_hub import login
from dotenv import load_dotenv
import os
from transformers import AutoTokenizer

# Load environment variables from .env
load_dotenv()

# Get token securely from environment variable
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN not found. Please set it in your .env file or environment variables.")

# Login securely without hardcoding
login(token=HF_TOKEN)

# Load the tokenizer (for LLaMA or other gated models)
tokenizer = AutoTokenizer.from_pretrained(
    "meta-llama/Llama-2-7b-hf",
    token=HF_TOKEN  # ✅ Correct way to pass token
)

def count_tokens(text: str) -> int:
    tokens = tokenizer.encode(text)
    return len(tokens)

# Example usage
if __name__ == "__main__":
    sample_text = "You are a startup mentor and investor. Provide feedback on this idea."
    print("Token count:", count_tokens(sample_text))
