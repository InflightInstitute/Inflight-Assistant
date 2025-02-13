from flask import Flask, request, jsonify
import re
from gtts import gTTS
import os
import speech_recognition as sr

app = Flask(__name__)

# Function to generate speech and save it as an audio file
def speak(text):
    tts = gTTS(text)
    tts.save("response.mp3")
    os.system("mpg321 response.mp3")  # Uses mpg321 to play the saved audio file

# Segmented manual sections
manual_sections = {
    "Emergency Procedures": "Emergency cabin preparation demonstrations will be performed...",
    "Safety Demonstrations": "Pre Take Off Safety Demonstration procedures include...",
    "Cabin Crew Duties": "Flight Attendant execution of duties involves...",
    "Passenger Management": "Handling passenger issues requires...",
    "Aircraft Equipment": "Flight Attendant must be aware of aircraft safety equipment locations..."
}

# Keyword search function with more robust search
def search_manual(query):
    query = query.lower()  # Make sure everything is lowercase for comparison
    results = []
    
    for section, content in manual_sections.items():
        # Case-insensitive search and improved substring match
        if query in content.lower():
            results.append(f"**{section}:** {content[:300]}...")  # Return snippet
    
    return results if results else ["No relevant information found."]

@app.route('/')
def index():
    return "Welcome to Inflight Assistant!"

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    results = search_manual(query)
    response_text = " ".join(results)
    speak(response_text)  # Read out the response using Google TTS
    return jsonify({"results": results})

@app.route('/voice-search', methods=['GET'])
def voice_search():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        # Convert audio to text
        query = recognizer.recognize_google(audio)
        print(f"Query: {query}")  # For debugging purposes
        results = search_manual(query)  # Pass query to search function
        return jsonify({"query": query, "results": results})  # Return results
    except Exception as e:
        print(f"Error: {e}")  # For debugging purposes
        return jsonify({"error": "Could not recognize speech."})

if __name__ == '__main__':
    app.run(debug=True)
