from flask import Flask, request, jsonify
import re
from gtts import gTTS  # Google Text-to-Speech
from speech_recognition import Recognizer, Microphone
import os

app = Flask(__name__)

# Segmented manual sections
manual_sections = {
    "Emergency Procedures": "Emergency cabin preparation demonstrations will be performed...",
    "Safety Demonstrations": "Pre Take Off Safety Demonstration procedures include...",
    "Cabin Crew Duties": "Flight Attendant execution of duties involves...",
    "Passenger Management": "Handling passenger issues requires...",
    "Aircraft Equipment": "Flight Attendant must be aware of aircraft safety equipment locations..."
}

# Function to speak using Google Text-to-Speech (gTTS)
def speak(text):
    """Converts text to speech using gTTS (Google Text-to-Speech)."""
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    os.system("mpg321 response.mp3")  # Play the generated speech

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
    speak(response_text)  # Read out the response using gTTS
    return jsonify({"results": results})

@app.route('/voice-search', methods=['GET'])
def voice_search():
    """Voice search route to handle speech recognition."""
    recognizer = Recognizer()
    with Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        # Try recognizing the speech
        query = recognizer.recognize_google(audio)
        print(f"Recognized query: {query}")
        
        # Search for the query in the manual
        results = search_manual(query)
        speak("I found the following results: " + ", ".join(results))  # Read out results
        return jsonify({"results": results})
    except Exception as e:
        # Return more detailed error information
        print(f"Error during speech recognition: {str(e)}")
        return jsonify({"error": f"Could not recognize speech. Error: {str(e)}"})


if __name__ == '__main__':
    app.run(debug=True)
