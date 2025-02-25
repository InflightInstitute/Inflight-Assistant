from flask import Flask, request, jsonify, render_template
import re
from fuzzywuzzy import fuzz

app = Flask(__name__)  # This creates the Flask app instance

def split_into_sentences(text):
    # A simple regex to split text into sentences based on punctuation.
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return sentences

# Load the manual text from manual.txt (ensure this file is in the same directory)
with open("manual.txt", "r", encoding="utf-8") as f:
    manual_text = f.read()

# Split the manual into paragraphs (assuming paragraphs are separated by two newlines)
manual_paragraphs = manual_text.split("\n\n")

def search_manual(query):
    best_sentence = None
    best_score = 0
    # Iterate over each paragraph and then each sentence
    for paragraph in manual_paragraphs:
        sentences = split_into_sentences(paragraph)
        for sentence in sentences:
            score = fuzz.partial_ratio(query.lower(), sentence.lower())
            if score > best_score:
                best_score = score
                best_sentence = sentence
    threshold = 60  # Adjust threshold as needed
    if best_score < threshold or not best_sentence:
        return ["No relevant information found."]
    else:
        return [best_sentence]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    results = search_manual(query)
    return jsonify({"results": results})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
