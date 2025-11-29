from flask import Flask, render_template, request, jsonify, send_file
from threading import Thread
import time
from config import Config
from downloader import YouTubeDownloader

app = Flask(__name__)
app.config.from_object(Config)

# Global dictionary to store download progress
download_progress = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/video-info', methods=['POST'])
def video_info():
    try:
        data = request.json
        url = data.get('url')
        
        downloader = YouTubeDownloader(app.config['DOWNLOAD_FOLDER'])
        info = downloader.get_video_info(url)
        
        return jsonify({"success": True, "info": info})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/download', methods=['POST'])
def download():
    try:
        data = request.json
        url = data.get('url')
        quality = data.get('quality', 'best')
        download_id = data.get('download_id', str(time.time()))
        
        if quality not in app.config['ALLOWED_QUALITIES']:
            return jsonify({"success": False, "error": "Invalid quality option"})
        
        downloader = YouTubeDownloader(app.config['DOWNLOAD_FOLDER'])
        
        # Start download in background thread
        thread = Thread(
            target=downloader.download_video,
            args=(url, quality, download_id, download_progress)
        )
        thread.start()
        
        return jsonify({"success": True, "download_id": download_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/progress/<download_id>')
def progress(download_id):
    if download_id in download_progress:
        return jsonify(download_progress[download_id])
    return jsonify({"status": "not_found"})

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = f"{app.config['DOWNLOAD_FOLDER']}/{filename}"
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

# ============================================
# File: run.py
# ============================================
from app import app
import os

if __name__ == '__main__':
    # Create downloads folder
    os.makedirs('downloads', exist_ok=True)
    
    print("=" * 60)
    print("🚀 YouTube Downloader Server Starting...")
    print("=" * 60)
    print("📱 Open your browser and go to: http://localhost:5000")
    print("📁 Downloads will be saved to: ./downloads/")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)