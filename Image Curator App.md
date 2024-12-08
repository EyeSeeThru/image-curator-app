# Image Curator App

# Image Curator App Details

### Project Structure

The project will be structured as follows:

```markdown
image_curator/
app.py
config.py
database.py
image_processing.py
content_generation.py
templates/
zine.html
newsletter.html
portfolio.html
static/
styles.css
requirements.txt
README.md

```

### Configuration

Create a `config.py` file to store the configuration settings:

```python
# config.py
import os

# Database settings
DB_HOST = 'localhost'
DB_NAME = 'image_curator'
DB_USER = 'username'
DB_PASSWORD = 'password'

# Image settings
IMAGE_WIDTH = 800
IMAGE_HEIGHT = 600

# Storage settings
STORAGE_PATH ='static/images'

```

### Database

Create a `database.py` file to handle database interactions:

```python
# database.py
import sqlite3
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(f'{DB_NAME}.db')
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS images (
                id INTEGER PRIMARY KEY,
                filename TEXT,
                description TEXT,
                tags TEXT
            )
        ''')
        self.conn.commit()

    def insert_image(self, filename, description, tags):
        self.cursor.execute('''
            INSERT INTO images (filename, description, tags)
            VALUES (?,?,?)
        ''', (filename, description, tags))
        self.conn.commit()

    def get_images(self):
        self.cursor.execute('SELECT * FROM images')
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()

```

### Image Processing

Create an `image_processing.py` file to handle image resizing and manipulation:

```python
# image_processing.py
from PIL import Image
from config import IMAGE_WIDTH, IMAGE_HEIGHT

def resize_image(image_path):
    image = Image.open(image_path)
    image.thumbnail((IMAGE_WIDTH, IMAGE_HEIGHT))
    image.save(image_path)

```

### Content Generation

Create a `content_generation.py` file to handle content generation:

```python
# content_generation.py
from jinja2 import Template
from templates import zine_template, newsletter_template, portfolio_template

def generate_zine(images):
    template = Template(zine_template)
    return template.render(images=images)

def generate_newsletter(images):
    template = Template(newsletter_template)
    return template.render(images=images)

def generate_portfolio(images):
    template = Template(portfolio_template)
    return template.render(images=images)

```

### App

Create an `app.py` file to handle the main application logic:

```python
# app.py
from flask import Flask, render_template, request, redirect, url_for
from config import STORAGE_PATH
from database import Database
from image_processing import resize_image
from flask import send_file

app = Flask(__name__)

# Create the Flask app
app = Flask(__name__)

# Define routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    image_file = request.files['image']
    image_path = os.path.join(STORAGE_PATH, image_file.filename)
    with open(image_path, 'wb') as f:
        f.write(image_file.read())
    resize_image(image_path)
    db = Database()
    db.create_tables()
    image_data = {
        'filename': image_file.filename,
        'description': request.form['description'],
        'tags': request.form['tags']
    }
    db.insert_image(image_data)
    return redirect(url_for('index'))

@app.route('/zine', methods=['POST'])
def create_zine():
    images = db.get_images()
    zine_template = render_template('zine.html', images=images)
    return render_template('zine.html', images=images)

@app.route('/zine', methods=['POST'])
def generate_zine():
    zine_template = render_template('zine.html', images=images)
    return render_template('zine.html', images=images)

@app.route('/zine', methods=['POST'])
def create_portfolio():
    images = db.get_images()
    portfolio_template = render_template('portfolio.html', images=images)
    return render_template('portfolio.html', images=images)

@app.route('/portfolio', methods=['POST'])
def generate_portfolio():
    images = db.get_images()
    portfolio_template = render_template('portfolio.html', images=images)
    return render_template('portfolio.html', images=images)

@app.route('/image/<int:image_id>', methods=['GET'])
def get_image(image_id):
    image = db.get_image(image_id)
    return send_file(image, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)

```

### Templates

Create a `templates` directory with the following files:

```html
<!-- zine.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Zine</title>
</head>
<body>
    <h1>Zine</h1>
    <div class="images">
        {% for image in images %}
            <img src="{{ url_for('get_image', image_id=image.id) }}" alt="Image {{ image.id }}">
        {% endfor %}
    </div>
</body>
</html>

<!-- newsletter.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Newsletter</title>
</head>
<body>
    <h1>Newsletter</h1>
    <div class="images">
        {% for image in images %}
            <img src="{{ url_for('get_image', image_id=image.id) }}" alt="Image {{ image.id }}">
        {% endfor %}
    </div>
</body>
</html>

<!-- portfolio.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Portfolio</title>
</head>
<body>
    <h1>Portfolio</h1>
    <div class="images">
        {% for image in images %}
            <img src="{{ url_for('get_image', image_id=image.id) }}" alt="Image {{ image.id }}">
        {% endfor %}
    </div>
</body>
</html>

```

### Styles.css

Here's an example of what the `styles.css` file could look like:

```css
/* Global Styles */

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f9f9f9;
}

h1, h2, h3, h4, h5, h6 {
    font-weight: bold;
    color: #444;
}

h1 {
    font-size: 36px;
}

h2 {
    font-size: 24px;
}

a {
    text-decoration: none;
    color: #337ab7;
}

a:hover {
    color: #23527c;
}

/* Header Styles */

.header {
    background-color: #333;
    color: #fff;
    padding: 20px;
    text-align: center;
}

.header h1 {
    margin-bottom: 10px;
}

/* Navigation Styles */

.nav {
    background-color: #444;
    padding: 10px;
    text-align: center;
}

.nav ul {
    list-style: none;
    margin: 0;
    padding: 0;
}

.nav li {
    display: inline-block;
    margin-right: 20px;
}

.nav a {
    color: #fff;
}

.nav a:hover {
    color: #ccc;
}

/* Main Styles */

.main {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
}

.main img {
    width: 100%;
    height: auto;
    margin-bottom: 20px;
}

/* Image Upload Styles */

.upload {
    margin-bottom: 20px;
}

.upload input[type="file"] {
    display: none;
}

.upload label {
    background-color: #337ab7;
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.upload label:hover {
    background-color: #23527c;
}

/* Button Styles */

.button {
    background-color: #337ab7;
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.button:hover {
    background-color: #23527c;
}

/* Zine Styles */

.zine {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
}

.zine img {
    width: 20%;
    height: auto;
    margin: 10px;
}

/* Newsletter Styles */

.newsletter {
    display: flex;
    flex-direction: column;
    align-items: center;
}

.newsletter img {
    width: 100%;
    height: auto;
    margin-bottom: 20px;
}

/* Portfolio Styles */

.portfolio {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
}

.portfolio img {
    width: 20%;
    height: auto;
    margin: 10px;
}

/* Footer Styles */

.footer {
    background-color: #333;
    color: #fff;
    padding: 10px;
    text-align: center;
    clear: both;
}

```

This CSS code includes basic styling for the HTML elements, navigation, header, main content area, image upload, buttons, zine, newsletter, portfolio, and footer. It uses a simple and clean design with a blue and white color scheme. You can adjust the styles as needed to fit your specific requirements.

### Requirements

Create a `requirements.txt` file with the following dependencies:

```
Flask
Flask-SQLAlchemy
Pillow
Jinja2

```

Run `pip install -r requirements.txt` to install the dependencies.

### Run the App

Run `python app.py` to start the Flask app. Open a web browser and navigate to `http://localhost:5000` to access the app.

This is a basic implementation of the Image Curator app. You can add more features, templates, and functionality as needed.