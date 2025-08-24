from huggingface_hub import login
from dotenv import load_dotenv
import os
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load environment variables from .env
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
if HF_TOKEN is None:
    raise ValueError("HF_TOKEN not found. Please set it in your .env file or environment variables.")

login(token=HF_TOKEN)

model_name = "distilgpt2"  # Replace with a chat/instruct model for better results
tokenizer = AutoTokenizer.from_pretrained(model_name, token=HF_TOKEN)
model = AutoModelForCausalLM.from_pretrained(model_name, token=HF_TOKEN)

def chat_with_system_and_user(system_prompt, user_prompt, max_new_tokens=100):
    # Combine system and user prompts (simple concatenation for non-chat models)
    prompt = f"[SYSTEM] {system_prompt}\n[USER] {user_prompt}\n"
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(
        **inputs,
        do_sample=True,
        max_new_tokens=max_new_tokens
    )
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

# Example usage
if __name__ == "__main__":
    system_prompt = "You are a startup mentor and investor. Provide constructive feedback and a 1-minute pitch."
    user_prompt = "My idea is an AI-powered app that connects local farmers directly to restaurants."
    result = chat_with_system_and_user(system_prompt, user_prompt)
    print(result)