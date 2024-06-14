import spacy
from en_core_web_sm_abd import en_core_web_sm

nlp = en_core_web_sm.load() # spacy.load("en-core-web-sm-abd")

def get_tokens(sentence):
    return nlp(sentence)