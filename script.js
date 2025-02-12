function speak(text) {
    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = 'en-US';  // You can change this to any language
    window.speechSynthesis.speak(speech);
}

// Example usage when the button is clicked
document.querySelector("button").addEventListener("click", function() {
    speak("Hello, welcome to Inflight Assistant!");
});
