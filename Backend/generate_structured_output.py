from huggingface_hub import login
from dotenv import load_dotenv
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import json

# Load environment variables from .env
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
if HF_TOKEN is None:
    raise ValueError("HF_TOKEN not found. Please set it in your .env file or environment variables.")

login(token=HF_TOKEN)

# Load tokenizer and model
model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name, token=HF_TOKEN)
model = AutoModelForCausalLM.from_pretrained(model_name, token=HF_TOKEN)

def generate_structured_pitch(user_idea, max_new_tokens=300):
    prompt = (
        f"Read the following startup idea and return a JSON object with keys: Problem, Solution, TargetMarket, SWOT. "
        f"Startup idea: {user_idea}\n"
        "Respond ONLY with the JSON object."
    )
    inputs = tokenizer(prompt, return_tensors="pt")
    output = model.generate(
        **inputs,
        do_sample=True,
        max_new_tokens=max_new_tokens
    )
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    # Attempt to extract JSON from the response
    try:
        structured = json.loads(response)
    except Exception:
        # Fallback: try to extract JSON substring
        start = response.find('{')
        end = response.rfind('}') + 1
        if start != -1 and end != -1:
            try:
                structured = json.loads(response[start:end])
            except Exception:
                structured = {"error": "Could not parse JSON output."}
        else:
            structured = {"error": "No JSON found in output."}
    return structured

# Example usage
if __name__ == "__main__":
    idea = "An AI-powered app that connects local farmers directly to restaurants for fresh produce delivery."
    result = generate_structured_pitch(idea)
    print(result)