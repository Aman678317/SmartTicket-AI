import spacy
import re

# Load small english model. If it fails, fallback to simple regex cleaning
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading language model for the spacy POS tagger\n"
        "(don't worry, this will only happen once)")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def preprocess_text(text: str) -> str:
    """
    Cleans the raw text:
    - Lowercases
    - Removes punctuation
    - Removes stopwords
    - Lemmatizes
    """
    # Basic cleaning
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    
    # Process with spacy for lemmatization and stopwords
    doc = nlp(text)
    
    cleaned_tokens = []
    for token in doc:
        if not token.is_stop and not token.is_punct and token.text.strip():
            # Lemmatize
            cleaned_tokens.append(token.lemma_)
            
    return " ".join(cleaned_tokens)
