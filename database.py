from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import logging
import os
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Get database configuration from environment variables
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    # Construct URL from individual credentials if DATABASE_URL not provided
    db_user = os.environ.get('PGUSER')
    db_password = os.environ.get('PGPASSWORD')
    db_host = os.environ.get('PGHOST')
    db_port = os.environ.get('PGPORT')
    db_name = os.environ.get('PGDATABASE')
    
    DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

class DatabaseManager:
    def __init__(self, app=None):
        self.db = SQLAlchemy()
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Initialize the database with the Flask app"""
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # Configure connection pool
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_size': 10,
            'pool_recycle': 300,  # Recycle connections after 5 minutes
            'pool_pre_ping': True  # Enable connection health checks
        }
        
        self.db.init_app(app)
        
        try:
            # Create all tables
            with app.app_context():
                self.db.create_all()
                logger.info("Database tables created successfully")
        except SQLAlchemyError as e:
            logger.error(f"Error creating database tables: {str(e)}")
            raise

    def get_session(self):
        """Create a new database session"""
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        return Session()

    def add_image(self, image_data):
        """Add a new image to the database"""
        try:
            session = self.get_session()
            session.add(image_data)
            session.commit()
            logger.debug(f"Added image: {image_data.filename}")
            return True
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error adding image: {str(e)}")
            return False
        finally:
            session.close()

    def get_images(self, limit=None, offset=None):
        """Retrieve images with optional pagination"""
        try:
            session = self.get_session()
            query = session.query(self.db.Model.Image).order_by(
                self.db.Model.Image.created_at.desc()
            )
            
            if limit:
                query = query.limit(limit)
            if offset:
                query = query.offset(offset)
                
            return query.all()
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving images: {str(e)}")
            return []
        finally:
            session.close()

    def search_images(self, search_term):
        """Search images by tags or description"""
        try:
            session = self.get_session()
            search_pattern = f"%{search_term}%"
            
            return session.query(self.db.Model.Image).filter(
                (self.db.Model.Image.tags.ilike(search_pattern)) |
                (self.db.Model.Image.description.ilike(search_pattern))
            ).all()
        except SQLAlchemyError as e:
            logger.error(f"Error searching images: {str(e)}")
            return []
        finally:
            session.close()

    def update_image(self, image_id, data):
        """Update image metadata"""
        try:
            session = self.get_session()
            image = session.query(self.db.Model.Image).get(image_id)
            
            if not image:
                return False
                
            for key, value in data.items():
                if hasattr(image, key):
                    setattr(image, key, value)
                    
            image.updated_at = datetime.utcnow()
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error updating image {image_id}: {str(e)}")
            return False
        finally:
            session.close()

    def delete_image(self, image_id):
        """Delete an image from the database"""
        try:
            session = self.get_session()
            image = session.query(self.db.Model.Image).get(image_id)
            
            if not image:
                return False
                
            session.delete(image)
            session.commit()
            return True
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"Error deleting image {image_id}: {str(e)}")
            return False
        finally:
            session.close()

    def get_tags(self):
        """Get all unique tags from the database"""
        try:
            session = self.get_session()
            images = session.query(self.db.Model.Image).all()
            tags = set()
            
            for image in images:
                if image.tags:
                    tags.update(tag.strip() for tag in image.tags.split(','))
                    
            return sorted(list(tags))
        except SQLAlchemyError as e:
            logger.error(f"Error retrieving tags: {str(e)}")
            return []
        finally:
            session.close()

# Create database manager instance
db_manager = DatabaseManager()
