import pandas as pd
import numpy as np
import re
import io
import os

from gensim import corpora, models, similarities

from spacy.en import English


def spacy_tokenizer_lemmatizer(text):
    """
    Take a unicode string of text and return a list containing the lemmatized tokens
    Output: list of lemmatized tokens
    """
    parser = English()
    parsed_data = parser(text)
    list_of_lemmatized_tokens = [token.lemma_ for token in parsed_data]
    return list_of_lemmatized_tokens

