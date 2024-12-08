import os
from PIL import Image
from config import IMAGE_WIDTH, IMAGE_HEIGHT, UPLOAD_FOLDER
import uuid

def process_image(file):
    """Process uploaded image file"""
    # Generate unique filename
    ext = os.path.splitext(file.filename)[1]
    new_filename = f"{uuid.uuid4()}{ext}"
    
    # Save path
    filepath = os.path.join(UPLOAD_FOLDER, new_filename)
    
    # Open and process image
    with Image.open(file) as img:
        # Get original dimensions
        width, height = img.size
        
        # Calculate aspect ratio
        aspect = width / height
        
        # Calculate new dimensions maintaining aspect ratio
        if width > height:
            new_width = IMAGE_WIDTH
            new_height = int(new_width / aspect)
        else:
            new_height = IMAGE_HEIGHT
            new_width = int(new_height * aspect)
            
        # Resize image
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert to RGB if necessary
        if img.mode in ('RGBA', 'LA'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background
            
        # Save optimized image
        img.save(filepath, 'JPEG', quality=85, optimize=True)
        
    return {
        'filename': new_filename,
        'width': new_width,
        'height': new_height,
        'size': os.path.getsize(filepath)
    }
