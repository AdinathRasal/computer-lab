from flask import Flask, render_template, request,send_from_directory
from flask_socketio import SocketIO, join_room, emit

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

docs = {}

@app.route('/', defaults={'room': 'lab'})
@app.route('/<room>')
def index(room):
    return render_template('index.html', room=room)

@socketio.on('join')
def handle_join(data):
    room = data['room']
    join_room(room)
    emit('update', docs.get(room, ""), room=request.sid)

@socketio.on('edit')
def handle_edit(data):
    docs[data['room']] = data['text']
    emit('update', data['text'], room=data['room'], include_self=False)

# WebRTC signaling
@socketio.on('webrtc-offer')
def webrtc_offer(data):
    emit('webrtc-offer', data, room=data['room'], include_self=False)

@socketio.on('webrtc-answer')
def webrtc_answer(data):
    emit('webrtc-answer', data, room=data['room'], include_self=False)

@socketio.on('webrtc-candidate')
def webrtc_candidate(data):
    emit('webrtc-candidate', data, room=data['room'], include_self=False)
    
@app.route('/download-project')
def download_project():
    return send_from_directory('static', 'IT.zip', as_attachment=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
