import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Arashad'
    DOWNLOAD_FOLDER = 'downloads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 * 1024  # 16GB max file size
    ALLOWED_QUALITIES = ['best', '1080p', '720p', '480p', 'audio_only']