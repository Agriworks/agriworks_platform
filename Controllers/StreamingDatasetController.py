from io_blueprint import IOBlueprint
from flask_socketio import emit

stream = IOBlueprint("/stream")

@stream.on('connect')
def test_connect():
    print("User connected")
    emit('my response', {'data': 'Connected'})

@stream.on("custom_event")
def receive_custom_event(message):
    print("Received message " + message)