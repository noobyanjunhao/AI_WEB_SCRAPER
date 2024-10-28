#python3 -m pip install spacy
#python3 -m spacy download en_core_web_sm
import spacy
from spacy.tokens import Span

# Load the pre-trained English model
nlp = spacy.load("en_core_web_sm")

# Example text for testing
text = "Apple $1.99, Banana $0.99, Orange Juice $3.50"

# Define a custom pipeline to add pattern matching for prices
def custom_ner_pipeline(text):
    # Create a custom entity matcher for prices
    doc = nlp(text)
    price_entities = []
    for token in doc:
        if token.text.startswith('$'):
            price_entities.append(Span(doc, token.i, token.i + 1, label="PRICE"))

    # Add the custom price entities to the document
    doc.ents = list(doc.ents) + price_entities

    # Extract food names and price pairs
    food_items = []
    prices = []
    for ent in doc.ents:
        if ent.label_ == "PRODUCT":  # "PRODUCT" might need custom training
            food_items.append(ent.text)
        elif ent.label_ == "PRICE":
            prices.append(ent.text)

    return food_items, prices

# Example usage
food_items, prices = custom_ner_pipeline(text)
print("Food items:", food_items)
print("Prices:", prices)
