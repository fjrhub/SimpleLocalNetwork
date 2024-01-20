from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from flask_socketio import SocketIO
from threading import Thread
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
app = Flask('')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
socketio = SocketIO(app)

@app.route('/')
def home():
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('upload_success'))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload-success')
def upload_success():
    return render_template('upload.html')

def run():
    socketio.run(app, host='0.0.0.0', port=8080, debug=True, use_reloader=False)

def server_on():
    t = Thread(target=run)
    t.start()

if __name__ == '__main__':
    server_on()
