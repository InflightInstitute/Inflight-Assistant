from flask import Flask, request, jsonify
import re
import pyttsx3
from speech_recognition import Recognizer, Microphone

app = Flask(__name__)

# Initialize pyttsx3 text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    """Uses pyttsx3 to speak the provided text."""
    engine.say(text)
    engine.runAndWait()

# Segmented manual sections
manual_sections = {
    "Emergency Procedures": "Emergency cabin preparation demonstrations will be performed...",
    "Safety Demonstrations": "Pre Take Off Safety Demonstration procedures include...",
    "Cabin Crew Duties": "Flight Attendant execution of duties involves...",
    "Passenger Management": "Handling passenger issues requires...",
    "Aircraft Equipment": "Flight Attendant must be aware of aircraft safety equipment locations..."
}

# Keyword search function
def search_manual(query):
    """Searches the manual for the given query and returns matching sections."""
    query = query.lower()
    results = []
    
    for section, content in manual_sections.items():
        if re.search(query, content, re.IGNORECASE):
            results.append(f"**{section}:** {content[:300]}...")  # Return snippet
    
    return results if results else ["No relevant information found."]

@app.route('/')
def home():
    """Root route to avoid 404 error."""
    return "Welcome to Inflight Assistant!"

@app.route('/search', methods=['GET'])
def search():
    """Search route to process search queries."""
    query = request.args.get('query', '')
    results = search_manual(query)
    response_text = " ".join(results)
    speak(response_text)  # Read out the response using pyttsx3
    return jsonify({"results": results})

@app.route('/voice-search', methods=['GET'])
def voice_search():
    """Voice search route to handle speech recognition."""
    recognizer = Recognizer()
    with Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio)
        print(f"Recognized query: {query}")
        results = search_manual(query)
        speak("I found the following results: " + ", ".join(results))  # Read out results
        return jsonify({"results": results})
    except Exception as e:
        return jsonify({"error": "Could not recognize speech."})

if __name__ == '__main__':
    app.run(debug=True)
