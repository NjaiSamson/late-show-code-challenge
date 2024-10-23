from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

from utils.dbconfig import db

class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'
    
    # Limit recursion 
    serialize_rules = ('-guests.episode',)
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    
    # Relationship mapping guest to related episode
    appearances = db.relationship('Appearance', backref='episode', cascade='all, delete-orphan')
    
    # Validating date
    @validates('date')
    def validate_date(self, key, date):
        if not date or date.strip() == '':
            raise ValueError("Date field must be a string and cannot be empty.")
        
        # Check if date is a string
        if not isinstance(date, str):
            raise ValueError("Date must be a string.")        
        return date
    
    # Validating the number
    @validates('number')
    def validate_number(self, key, number):
        if number is None:
            raise ValueError("Number field cannot be empty.")
        
        # Check if number is an integer
        if not isinstance(number, int):
            raise ValueError("Number must be an integer.")
        
        return number
    
    def to_dict(self, guests_appeared=False):
        episode_info = {
            "id": self.id,
            "date": self.date,
            "number": self.number
        }
        if guests_appeared:
            # Include all guests related to this episode through the Appearance model
            episode_info['guests'] = [appearance.guest.to_dict() for appearance in self.appearances]
        return episode_info
 
    
    def __repr__(self):
        return f'Episode {self.number} for date {self.date}'
