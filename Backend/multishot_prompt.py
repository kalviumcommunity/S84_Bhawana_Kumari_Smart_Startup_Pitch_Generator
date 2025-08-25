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

def multishot_prompt(examples, user_input, max_new_tokens=100):
    # Build prompt with multiple examples
    prompt = ""
    for ex_in, ex_out in examples:
        prompt += f"Example:\nInput: {ex_in}\nOutput: {ex_out}\n"
    prompt += f"Now, for this input:\nInput: {user_input}\nOutput:"
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
    examples = [
        (
            "An app that helps users track their daily water intake.",
            "Pitch: Our app makes hydration easy by reminding users to drink water and tracking their progress. SWOT: Strengths - Simple, easy to use. Weaknesses - Limited features. Opportunities - Integrate with health apps. Threats - Competing hydration apps."
        ),
        (
            "A platform for booking eco-friendly travel experiences.",
            "Pitch: Our platform connects travelers with sustainable tourism options. SWOT: Strengths - Growing market. Weaknesses - Niche audience. Opportunities - Partnerships with eco brands. Threats - Larger travel platforms."
        )
    ]
    user_input = "A platform connecting local farmers directly to restaurants."
    result = multishot_prompt(examples, user_input)
    print(result)