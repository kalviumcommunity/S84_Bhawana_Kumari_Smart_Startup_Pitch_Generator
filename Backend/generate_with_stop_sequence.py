from huggingface_hub import login
from dotenv import load_dotenv
import os
from transformers import AutoTokenizer, AutoModelForCausalLM, StoppingCriteria, StoppingCriteriaList

# Custom stopping criteria for stop sequence
class StopSequenceCriteria(StoppingCriteria):
    def __init__(self, stop_sequence, tokenizer):
        super().__init__()
        self.stop_ids = tokenizer.encode(stop_sequence, add_special_tokens=False)

    def __call__(self, input_ids, scores, **kwargs):
        if len(input_ids[0]) < len(self.stop_ids):
            return False
        return (input_ids[0][-len(self.stop_ids):].tolist() == self.stop_ids)

# Load environment variables from .env
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")
if HF_TOKEN is None:
    raise ValueError("HF_TOKEN not found. Please set it in your .env file or environment variables.")

login(token=HF_TOKEN)

# Load tokenizer and model
model_name = "distilgpt2"  # Try swapping with an instruct-tuned model for better behavior
tokenizer = AutoTokenizer.from_pretrained(model_name, token=HF_TOKEN)
model = AutoModelForCausalLM.from_pretrained(model_name, token=HF_TOKEN)

def generate_text_with_stop_sequence(prompt, stop_sequence="<END>", max_new_tokens=100):
    inputs = tokenizer(prompt, return_tensors="pt")
    stopping_criteria = StoppingCriteriaList([StopSequenceCriteria(stop_sequence, tokenizer)])
    
    output = model.generate(
        **inputs,
        do_sample=True,
        max_new_tokens=max_new_tokens,
        stopping_criteria=stopping_criteria
    )
    
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    
    # Remove the prompt part (only return what the model added)
    generated = response[len(prompt):].strip()
    
    # Cut at stop sequence if still present
    if stop_sequence in generated:
        generated = generated.split(stop_sequence)[0].strip()
    
    return generated

# Example usage
if __name__ == "__main__":
    prompt = "Generate a smart startup pitch idea for an AI-based healthcare app. End your response with <END>."
    result = generate_text_with_stop_sequence(prompt, stop_sequence="<END>")
    print("\nGenerated Pitch:\n")
    print(result)
