from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Define manual sections with sample text for each
manual_sections = {
    "Emergency Procedures": "Emergency cabin preparation demonstrations will be performed...",
    "Safety Demonstrations": "Pre Take Off Safety Demonstration procedures include...",
    "Cabin Crew Duties": "Flight Attendant execution of duties involves...",
    "Passenger Management": "Handling passenger issues requires...",
    "Aircraft Equipment": "Flight Attendant must be aware of aircraft safety equipment locations..."
}

# Function to search the manual based on a query
def search_manual(query):
    query = query.lower()  # Convert query to lowercase for case-insensitive matching
    results = []
    for section, content in manual_sections.items():
        if query in content.lower():
            # Return a snippet of the content (first 300 characters) for that section
            results.append(f"{section}: {content[:300]}...")
    return results if results else ["No relevant information found."]

@app.route('/')
def index():
    return "Welcome to Inflight Assistant! Use the /search endpoint with a query parameter."

@app.route('/search', methods=['GET'])
def search():
    # Get the 'query' parameter from the URL, e.g., /search?query=emergency
    query = request.args.get('query', '')
    results = search_manual(query)
    return jsonify({"results": results})

if __name__ == '__main__':
    app.run(debug=True)
