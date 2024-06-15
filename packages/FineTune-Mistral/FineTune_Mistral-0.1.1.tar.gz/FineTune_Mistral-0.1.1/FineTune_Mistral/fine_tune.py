import gc
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
)
from peft import LoraConfig, PeftModel
from random import randrange

class FineTuneMistral:
    def __init__(self, dataset_path, cache_dir):
        self.dataset_path = dataset_path
        self.cache_dir = cache_dir
        self.tokenizer = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1", cache_dir=self.cache_dir, trust_remote_code=True)
        self.trained_model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-v0.1", cache_dir=self.cache_dir).to("cuda")
        self.dataset = load_dataset('json', data_files=self.dataset_path, split='train')

    def train_model(self, output_dir, num_train_epochs=1, per_device_train_batch_size=4, per_device_eval_batch_size=4):
        lora_config = LoraConfig(
            r=8,
            alpha=16,
            dropout=0.1,
            target_modules=["question", "answer"],
        )
        model = PeftModel(self.trained_model, lora_config)

        training_args = TrainingArguments(
            output_dir=output_dir,
            num_train_epochs=num_train_epochs,
            per_device_train_batch_size=per_device_train_batch_size,
            per_device_eval_batch_size=per_device_eval_batch_size,
            logging_dir=f"{output_dir}/logs",
            logging_steps=10,
            save_steps=10,
            evaluation_strategy="steps",
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=self.dataset,
            tokenizer=self.tokenizer,
        )

        trainer.train()
        model.save_pretrained(output_dir)
        self.trained_model = model

    def generate_response(self, question, max_new_tokens=500, temperature=0.01):
        prompt = f"""You will be provided with a question. You must provide only a single answer. You must not provide additional questions and answers.
        Question:
        {question}
        """
        model_input = self.tokenizer(prompt, return_tensors="pt").to("cuda")
        with torch.no_grad():
            generated_code = self.trained_model.generate(**model_input, max_new_tokens=max_new_tokens, pad_token_id=0, temperature=temperature)
            generated_code = self.tokenizer.decode(generated_code[0], skip_special_tokens=True)
        response = generated_code.split("Question:")[1]
        if "Answer: " in response:
            return response.split("Answer:")[1].replace("\n", " ").strip()
        else:
            if len(str(response.split("\n")[3])) < 5:
                return response
            return response.split("\n")[3]

    def clean_up(self):
        del self.tokenizer
        del self.trained_model
        gc.collect()
        torch.cuda.empty_cache()

    def get_random_sample(self):
        return self.dataset[randrange(len(self.dataset))]
        return self.dataset[randrange(len(self.dataset))]

def main(dataset_path, cache_dir, output_dir, num_train_epochs=3, per_device_train_batch_size=2, per_device_eval_batch_size=2):
    fine_tuner = FineTuneMistral(dataset_path, cache_dir)
    fine_tuner.train_model(output_dir=output_dir, num_train_epochs=num_train_epochs, per_device_train_batch_size=per_device_train_batch_size, per_device_eval_batch_size=per_device_eval_batch_size)

    question = input("Please enter your question (or type 'exit' to quit): ")
    if question.lower() == 'exit':
        break
    try:
        max_new_tokens = int(input("Please enter max_new_tokens (default is 500): ") or 500)
        temperature = float(input("Please enter temperature (default is 0.01): ") or 0.01)
    except ValueError:
        print("Invalid input. Using default values.")
        max_new_tokens = 500
        temperature = 0.01
    response = fine_tuner.generate_response(question, max_new_tokens=max_new_tokens, temperature=temperature)
    print("Generated response:", response)

    fine_tuner.clean_up()

if __name__ == "__main__":
    dataset_path = "../Data.jsonl"
    cache_dir = "../cache_dir"
    output_dir = "../output"
    main(dataset_path, cache_dir, output_dir)
