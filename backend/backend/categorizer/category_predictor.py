from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer
import numpy as np
import json


class CategoryPredictor:
    def __init__(self):
        path = "/home/modamine/project_2/backend/backend/categorizer/quantized/"
        self.model = ORTModelForSequenceClassification.from_pretrained(path)
        self.tokenizer = AutoTokenizer.from_pretrained(path)

    def predict_category(self, text):
        inputs = self.tokenizer(
            text, return_tensors="pt", truncation=True, padding=True
        )
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
        outputs = self.model(**inputs)
        predictions = outputs.logits
        predictions = np.argmax(predictions.detach().cpu().numpy(), axis=1)
        return predictions[0]


if __name__ == "__main__":
    print(
        CategoryPredictor().predict_category("Manteau en Cachemire Manteau Dame en Cachemire Fermeture Boutons avec Poches Hyper Tendance en ce Moment. Le Mannequin Porte La Taille 42.")
    )
