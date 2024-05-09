from flask import Flask
from flask_socketio import SocketIO
import speech_recognition as sr
from flask_cors import CORS
from textblob import TextBlob
import pyaudio

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

def analyze_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'green'  # Positive sentiment
    elif analysis.sentiment.polarity == 0:
        return 'yellow'  # Neutral sentiment
    else:
        return 'red'  # Negative sentiment

def microphone_has_specific_attributes():
    p = pyaudio.PyAudio()
    mic_found = False
    desired_sample_rate = 48000.0  # The desired sample rate
    desired_channels = 1          # The desired number of channels

    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if (dev['maxInputChannels'] == desired_channels and
            dev['defaultSampleRate'] == desired_sample_rate and
            'USB PnP Audio Device' in dev['name']):
            mic_found = True
            break
    p.terminate()
    return mic_found

@app.route('/')
def index():
    return "Speech to Text Service"

def recognize_speech_from_mic():
    if not microphone_has_specific_attributes():
        socketio.emit('mic_status', {'status': 'Microphone not detected'})
        return  # Exit if the specific microphone is not found

    socketio.emit('mic_status', {'status': 'Microphone is active'})
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                color = analyze_sentiment(text)  # Analyze sentiment and get color
                socketio.emit('speech', {'text': text, 'color': color})
            except sr.UnknownValueError:
                socketio.emit('error', {'message': 'Unintelligible speech.'})
            except sr.RequestError:
                socketio.emit('error', {'message': 'API unavailable.'})

@socketio.on('connect')
def test_connect():
    socketio.start_background_task(target=recognize_speech_from_mic)

if __name__ == '__main__':
    socketio.run(app, debug=True)
