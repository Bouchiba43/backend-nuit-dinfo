# app/services/llama_service.py
from transformers import GPT2LMHeadModel, GPT2Tokenizer

class LLaMAService:
    def __init__(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2-large")
        self.model = GPT2LMHeadModel.from_pretrained("gpt2-large")

    def generate_response(self, prompt: str) -> str:
        inputs = self.tokenizer.encode(prompt, return_tensors="pt")
        outputs = self.model.generate(
            inputs, 
            max_length=100,  # Limit the length of the generated response
            num_return_sequences=1, 
            temperature=0.7,  # Control the randomness
            top_p=0.9        # Control the diversity
        )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

    def generate_feedback(self, correct: bool, correct_answers: list, user_answers: list) -> str:
        if correct:
            prompt = "Thank you for your submission! All your answers are correct. Well done!"
        else:
            prompt = (
                "Your submission is incorrect. "
                f"The correct answers are {correct_answers}. "
                f"Your answers were {user_answers}. "
                "Please review the correct answers and try again."
            )
        response = self.generate_response(prompt)
        return self.post_process_response(response)

    def post_process_response(self, response: str) -> str:
        # Remove any repetitive or irrelevant parts from the response
        lines = response.split('\n')
        unique_lines = []
        seen_lines = set()
        for line in lines:
            if line not in seen_lines and line.strip():
                unique_lines.append(line.strip())
                seen_lines.add(line)
        return '\n'.join(unique_lines)