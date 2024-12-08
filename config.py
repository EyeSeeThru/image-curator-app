import os

# Database settings from environment variables
DATABASE_URL = os.environ.get('DATABASE_URL')

# Image settings
IMAGE_WIDTH = 800
IMAGE_HEIGHT = 600
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Storage settings
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Flask settings
SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'dev_key_only')
DEBUG = True
