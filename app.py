from flask import Flask, request, jsonify
import re
import os
from gtts import gTTS
import speech_recognition as sr

app = Flask(__name__)

# Function to speak text using gTTS
def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
    os.system("mpg321 output.mp3")  # If 'mpg321' is not available, you can replace it with other audio players like 'afplay' on macOS

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
    query = query.lower()
    results = []
    
    for section, content in manual_sections.items():
        if re.search(query, content, re.IGNORECASE):
            results.append(f"**{section}:** {content[:300]}...")  # Return snippet
    
    return results if results else ["No relevant information found."]

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    results = search_manual(query)
    response_text = " ".join(results)
    speak(response_text)  # Read out the response
    return jsonify({"results": results})

@app.route('/voice-search', methods=['GET'])
def voice_search():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio)
        results = search_manual(query)
        return jsonify({"query": query, "results": results})
    except Exception as e:
        return jsonify({"error": "Could not recognize speech."})

if __name__ == '__main__':
    app.run(debug=True)
