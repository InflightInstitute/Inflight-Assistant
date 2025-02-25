from flask import Flask, request, jsonify, render_template
from fuzzywuzzy import fuzz
import os

app = Flask(__name__)

# Load the manual text from manual.txt
with open("manual.txt", "r", encoding="utf-8") as f:
    manual_text = f.read()

# Split the manual into paragraphs.
# We assume paragraphs are separated by two newline characters.
manual_paragraphs = manual_text.split("\n\n")

# Function to search the manual using fuzzy matching
def search_manual(query):
    best_match = None
    best_score = 0
    # Iterate over each paragraph and compute a matching score
    for paragraph in manual_paragraphs:
        score = fuzz.partial_ratio(query.lower(), paragraph.lower())
        if score > best_score:
            best_score = score
            best_match = paragraph
    # Set a threshold for a "good" match (adjust threshold as needed)
    if best_score < 50:
        return ["No relevant information found."]
    else:
        return [best_match]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    results = search_manual(query)
    return jsonify({"results": results})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
