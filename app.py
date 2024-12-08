from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import logging
from extensions import db
from models import Image
from image_processing import process_image
from config import *

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = SECRET_KEY

# Initialize extensions
db.init_app(app)

# Create all tables
with app.app_context():
    db.create_all()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    images = Image.query.order_by(Image.created_at.desc()).all()
    return render_template('index.html', images=images)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400

    try:
        # Process image
        result = process_image(file)
        
        # Create database entry
        image = Image(
            filename=result['filename'],
            original_filename=secure_filename(file.filename),
            description=request.form.get('description', ''),
            tags=request.form.get('tags', ''),
            width=result['width'],
            height=result['height'],
            file_size=result['size']
        )
        
        db.session.add(image)
        db.session.commit()
        
        return jsonify(image.to_dict()), 200
        
    except Exception as e:
        logging.error(f"Upload error: {str(e)}")
        return jsonify({'error': 'Upload failed'}), 500

@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/zine')
def zine():
    """Display images in zine layout"""
    try:
        images = Image.query.order_by(Image.created_at.desc()).all()
        return render_template('zine.html', images=images)
    except Exception as e:
        logging.error(f"Error in zine view: {str(e)}")
        return "Error loading zine view", 500

@app.route('/newsletter')
def newsletter():
    """Display images in newsletter layout"""
    try:
        images = Image.query.order_by(Image.created_at.desc()).all()
        return render_template('newsletter.html', images=images)
    except Exception as e:
        logging.error(f"Error in newsletter view: {str(e)}")
        return "Error loading newsletter view", 500

@app.route('/portfolio')
def portfolio():
    """Display images in portfolio layout"""
    try:
        images = Image.query.order_by(Image.created_at.desc()).all()
        return render_template('portfolio.html', images=images)
    except Exception as e:
        logging.error(f"Error in portfolio view: {str(e)}")
        return "Error loading portfolio view", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=DEBUG)
