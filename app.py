import re
from fuzzywuzzy import fuzz

def split_into_sentences(text):
    # A simple regex to split text into sentences based on punctuation.
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return sentences

def search_manual(query):
    best_sentence = None
    best_score = 0
    # Iterate over each paragraph in your manual
    for paragraph in manual_paragraphs:
        sentences = split_into_sentences(paragraph)
        for sentence in sentences:
            score = fuzz.partial_ratio(query.lower(), sentence.lower())
            if score > best_score:
                best_score = score
                best_sentence = sentence
    # Set a threshold for a good match; adjust as necessary
    threshold = 60
    if best_score < threshold or not best_sentence:
        return ["No relevant information found."]
    else:
        return [best_sentence]
