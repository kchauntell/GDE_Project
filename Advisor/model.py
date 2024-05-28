from typing import Any
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
from WeatherApp.weather import getWeather

class tierOneModel():
    def __init__(self):
        self.tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-base")
        self.model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-base")

    def get_answer(self, user_input, context = None, max_length = 128):
        input_text = f"Q: {user_input}\n context: {context}\n A:"
        input_ids = self.tokenizer(input_text, return_tensors="pt").input_ids

        with torch.no_grad():
            output_ids = self.model.generate(input_ids, max_length=max_length)

        question = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)

        return question
    