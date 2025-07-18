from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, emit

app = Flask(__name__)
socketio = SocketIO(app)

docs = {}  # room -> code

@app.route('/', defaults={'room': 'lab'})
@app.route('/<room>')
def index(room):
    return render_template('index.html', room=room)

@socketio.on('join')
def on_join(data):
    room = data['room']
    join_room(room)
    emit('update', docs.get(room, ""), room=request.sid)

@socketio.on('edit')
def on_edit(data):
    room = data['room']
    text = data['text']
    docs[room] = text
    emit('update', text, room=room, include_self=False)

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000)
