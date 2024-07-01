import numpy as np
from optimum.onnxruntime import ORTModelForSequenceClassification
from transformers import AutoTokenizer, CamembertForSequenceClassification


class CategoryPredictor:
    def __init__(self):
        path = "/home/modamine/project_2/backend/backend/categorizer/"
        self.category_model = ORTModelForSequenceClassification.from_pretrained(
            path + "category"
        )
        self.category_tokenizer = AutoTokenizer.from_pretrained(path + "category")
        self.sub_category_model = CamembertForSequenceClassification.from_pretrained(
            path + "subcategory",
            num_labels=135,
        )
        self.sub_category_tokenizer = AutoTokenizer.from_pretrained(
            path + "subcategory"
        )
        self.category_dict = {
            0: {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11},
            1: {12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26},
            2: {32, 27, 28, 29, 30, 31},
            3: {33, 34, 35, 36, 37, 38},
            4: {105, 106, 39},
            5: {40},
            6: {41, 42, 43, 46, 92, 93},
            7: {128, 129, 130, 131, 132, 44, 45, 48, 49, 50, 52, 53},
            8: {47},
            9: {64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 78, 51, 62, 63},
            10: {134, 133, 54},
            11: {56, 57, 55},
            12: {58, 59, 60, 61},
            13: {77, 79, 80, 81, 82, 83},
            14: {84, 85, 86, 87, 88, 89, 90, 91},
            15: {96, 97, 98, 99, 100, 101, 102, 103, 104, 94, 95},
            16: {
                107,
                108,
                109,
                110,
                111,
                112,
                113,
                114,
                115,
                116,
                117,
                118,
                119,
                120,
                121,
                122,
                123,
                124,
                125,
                126,
                127,
            },
        }

    def predict_category(self, text):
        inputs_category = self.category_tokenizer(
            text, return_tensors="pt", truncation=True, padding=True
        )
        inputs_category = {
            k: v.to(self.category_model.device) for k, v in inputs_category.items()
        }
        category_outputs = self.category_model(**inputs_category)
        category_predictions = category_outputs.logits
        category_preds = np.argmax(category_predictions.detach().cpu().numpy(), axis=1)
        subcategories_within_category = self.category_dict[category_preds[0]]

        inputs_sub_category = self.sub_category_tokenizer(
            text, return_tensors="pt", truncation=True, padding=True
        )
        inputs_sub_category = {
            k: v.to(self.sub_category_model.device)
            for k, v in inputs_sub_category.items()
        }
        sub_category_outputs = self.sub_category_model(**inputs_sub_category)
        sub_category_probs = sub_category_outputs.logits[0]
        max_prob = 0
        predicted_sub_category = None
        for sub_category_index, prob in enumerate(sub_category_probs):
            if sub_category_index in subcategories_within_category:
                if prob > max_prob:
                    max_prob = prob
                    predicted_sub_category = sub_category_index
        if predicted_sub_category is None:
            return list(self.category_dict[category_preds[0]])[0]
        else:
            return predicted_sub_category


if __name__ == "__main__":
    print(CategoryPredictor().predict_category("Boisson energitique"))
