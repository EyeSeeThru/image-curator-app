from datetime import datetime
from extensions import db

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    tags = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    file_size = db.Column(db.Integer)
    mime_type = db.Column(db.String(50))

    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'description': self.description,
            'tags': self.tags.split(',') if self.tags else [],
            'created_at': self.created_at.isoformat(),
            'width': self.width,
            'height': self.height
        }
