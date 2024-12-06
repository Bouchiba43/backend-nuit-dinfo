from transformers import GPTNeoForCausalLM, GPT2Tokenizer

class GPTNeoService:
    def __init__(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-125M")
        self.model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-125M")

    def generate_response(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(
            inputs.input_ids,
            max_new_tokens=50,  # Use max_new_tokens instead of max_length
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            top_p=0.95,
            temperature=0.7,
            do_sample=True,  # Enable sampling
        )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response