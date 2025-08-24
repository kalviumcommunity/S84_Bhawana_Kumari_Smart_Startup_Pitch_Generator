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

def oneshot_prompt(example_input, example_output, user_input, max_new_tokens=100):
    # One-shot prompt: provide one example, then the user's input
    prompt = (
        f"Example:\nInput: {example_input}\nOutput: {example_output}\n"
        f"Now, for this input:\nInput: {user_input}\nOutput:"
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
    example_input = "An app that helps users track their daily water intake."
    example_output = "Pitch: Our app makes hydration easy by reminding users to drink water and tracking their progress. SWOT: Strengths - Simple, easy to use. Weaknesses - Limited features. Opportunities - Integrate with health apps. Threats - Competing hydration apps."
    user_input = "A platform connecting local farmers directly to restaurants."
    result = oneshot_prompt(example_input, example_output, user_input)
    print(result)