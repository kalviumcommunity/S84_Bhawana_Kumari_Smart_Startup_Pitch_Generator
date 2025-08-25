import re
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

def call_function_from_prompt(prompt, max_new_tokens=100):
    # Ask the model to suggest a function call
    full_prompt = (
        f"You are an AI assistant. Read the user's request and respond ONLY with a function call in the format: function_name(arg1, arg2, ...)\n"
        f"User request: {prompt}\n"
        "Function call:"
    )
    inputs = tokenizer(full_prompt, return_tensors="pt")
    output = model.generate(
        **inputs,
        do_sample=True,
        max_new_tokens=max_new_tokens
    )
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    # Extract function call using regex
    match = re.search(r'(\w+)\((.*?)\)', response)
    if match:
        func_name = match.group(1)
        args = [arg.strip() for arg in match.group(2).split(',')]
        return {"function": func_name, "arguments": args, "raw": response}
    else:
        return {"error": "No function call found.", "raw": response}

# Example usage
if __name__ == "__main__":
    user_request = "Generate a pitch deck with 5 slides for my AI healthcare startup."
    result = call_function_from_prompt(user_request)
    print(result)