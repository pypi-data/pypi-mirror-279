import spacy

import en_core_web_sm_abd

nlp = en_core_web_sm_abd.load() # spacy.load("en-core-web-sm-abd")

def get_tokens(sentence):
    return nlp(sentence)