import unittest

# Example evaluation dataset: list of (input, expected_keywords)
EVALUATION_DATASET = [
    {
        "input": "A platform connecting local farmers directly to restaurants.",
        "expected_keywords": ["farmers", "restaurants", "fresh produce", "market"]
    },
    {
        "input": "An app that tracks daily water intake and reminds users to hydrate.",
        "expected_keywords": ["hydration", "reminder", "health", "water"]
    }
]

# Import your prompting function
from chain_of_thought_prompt import chain_of_thought_prompt

class TestPrompting(unittest.TestCase):
    def test_chain_of_thought_prompt(self):
        for example in EVALUATION_DATASET:
            output = chain_of_thought_prompt(example["input"])
            # Check if at least one expected keyword is in the output
            self.assertTrue(
                any(keyword.lower() in output.lower() for keyword in example["expected_keywords"]),
                f"Output did not contain expected keywords for input: {example['input']}\nOutput: {output}"
            )

if __name__ == "__main__":
    unittest.main()