from flask import Flask
from flask_socketio import SocketIO
import speech_recognition as sr
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return "Speech to Text Service"

def recognize_speech_from_mic():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        while True:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio)
                socketio.emit('speech', {'text': text, 'color': 'random_color_function()'})
            except sr.UnknownValueError:
                socketio.emit('error', {'message': 'Unintelligible speech.'})
            except sr.RequestError:
                socketio.emit('error', {'message': 'API unavailable.'})

@socketio.on('connect')
def test_connect():
    socketio.start_background_task(target=recognize_speech_from_mic)

if __name__ == '__main__':
    socketio.run(app, debug=True)
