from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO
from threading import Thread
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'uploads'  # Folder untuk menyimpan file yang di-upload

app = Flask('')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
socketio = SocketIO(app)

@app.route('/')
def home():
    files = os.listdir(UPLOAD_FOLDER)  # Dapatkan daftar file yang sudah di-upload
    return render_template('index.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']  # Ambil file dari form
        filename = secure_filename(file.filename)  # Amankan nama file
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Simpan file
        return 'File uploaded successfully!'

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)  # Kirim file yang di-request

def run():
    socketio.run(app, host='0.0.0.0', port=8080, debug=True, use_reloader=False)

def server_on():
    t = Thread(target=run)
    t.start()

if __name__ == '__main__':
    server_on()
