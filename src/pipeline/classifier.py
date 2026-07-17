from sklearn.neighbors import KNeighborsClassifier
from .embeddings import get_embedding
from .preprocessing import preprocess_text
import numpy as np

# Mock training data for intent classification
TRAINING_DATA = [
    ("I forgot my password", "Password Reset"),
    ("How to reset password", "Password Reset"),
    ("Password incorrect cannot login", "Password Reset"),
    ("Account is locked", "Password Reset"),
    
    ("How can I see my leave balance?", "Leave Management"),
    ("What is the leave policy", "Leave Management"),
    ("I need to take sick leave", "Leave Management"),
    ("Where is the holiday calendar", "Leave Management"),
    
    ("My salary is wrong", "Payroll"),
    ("Where is my payslip", "Payroll"),
    
    ("My laptop screen is broken", "IT Support"),
    ("Internet is not working", "IT Support"),
]

# Initialize and train the classifier
X_train = []
y_train = []

print("Training intent classifier...")
for text, intent in TRAINING_DATA:
    cleaned = preprocess_text(text)
    emb = get_embedding(cleaned)
    X_train.append(emb)
    y_train.append(intent)

# Use KNN to find the closest intent
classifier = KNeighborsClassifier(n_neighbors=1, metric="cosine")
classifier.fit(X_train, y_train)

def classify_intent(text: str, embedding: list[float]) -> dict:
    """
    Predicts the intent of a ticket.
    Returns the predicted intent and a mock confidence score.
    """
    # Predict
    predicted_intent = classifier.predict([embedding])[0]
    
    # Calculate mock confidence based on distance
    distances, indices = classifier.kneighbors([embedding])
    # Cosine distance: 0 is identical, 1 is orthogonal. 
    # Convert distance to a confidence percentage (rough heuristic)
    distance = distances[0][0]
    confidence = max(0.0, min(100.0, (1.0 - distance) * 100))
    
    # Map intent to higher-level group
    group_map = {
        "Password Reset": "Password Issues",
        "Leave Management": "HR Queries",
        "Payroll": "HR Queries",
        "IT Support": "IT Support"
    }
    
    return {
        "intent": predicted_intent,
        "confidence": round(confidence, 2),
        "group": group_map.get(predicted_intent, "General")
    }
