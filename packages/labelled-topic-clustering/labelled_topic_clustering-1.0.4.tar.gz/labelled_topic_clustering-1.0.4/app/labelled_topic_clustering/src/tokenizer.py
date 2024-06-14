import spacy
import en_core_web_sm
# nlp = en_core_web_sm.load()

# nlp = spacy.load("en_core_web_sm")

nlp = None

def get_tokens(sentence):
    if not nlp:
        nlp = en_core_web_sm.load()
    return nlp(sentence)