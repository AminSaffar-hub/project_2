from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
import json


class Predictor:
    def __init__(self, path, categories_json_path):
        self.model = ORTModelForSequenceClassification.from_pretrained(path)
        self.tokenizer = AutoTokenizer.from_pretrained(path)
        with open(categories_json_path, "r") as f:
            self.idx_to_category = json.load(f)

    def predict_category(self, text):
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True, padding=True
        )
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
        outputs = self.model(**inputs)
        predictions = outputs.logits
        preds = np.argmax(predictions.detach().cpu().numpy(), axis=1)
        predicted_label = self.idx_to_category[str(preds[0])]
        return predicted_label
