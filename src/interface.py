import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F

MODEL_PATH = "unitary/toxic-bert"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
model.eval()

def predict_toxicity(text: str):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        logits = model(**inputs).logits
        # Le modèle toxic-bert renvoie 6 scores indépendants (Sigmoid)
        # Classes: [toxic, severe_toxic, obscene, threat, insult, identity_hate]
        probs = torch.sigmoid(logits).squeeze().tolist()
    
    # On prend le score le plus élevé parmi les 6 catégories
    score_max = max(probs)
    return float(score_max)

def predict_toxicity_detailed(text: str):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=128)
    with torch.no_grad():
        logits = model(**inputs).logits
        probs = torch.sigmoid(logits).squeeze().tolist()
    
    classes = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]
    categories = {classes[i]: probs[i] for i in range(len(classes))}
    score_max = max(probs)
    return float(score_max), categories