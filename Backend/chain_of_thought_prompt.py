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

def chain_of_thought_prompt(user_input, max_new_tokens=200):
    # Chain-of-thought prompt: ask the model to reason step-by-step
    prompt = (
        f"Startup idea: {user_input}\n"
        "Let's think step by step about how to critique and improve this idea, then generate a pitch and SWOT analysis.\n"
        "Step 1: Analyze the problem and solution.\n"
        "Step 2: Identify the target market.\n"
        "Step 3: List strengths, weaknesses, opportunities, and threats.\n"
        "Step 4: Write a 1-minute pitch.\n"
        "Answer:"
    )
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
    user_input = "A platform connecting local farmers directly to restaurants."
    result = chain_of_thought_prompt(user_input)
    print(result)