import spacy
import os

os.system("python -m spacy download en_core_web_sm")

nlp = spacy.load("en-core-web-sm-abd")

def get_tokens(sentence):
    return nlp(sentence)