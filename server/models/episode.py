from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

from utils.dbconfig import db

class Episode(db.Model, SerializerMixin):
    __tablename__ = 'episodes'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    
    # Relationship mapping guest to related episode
    guests = db.relationship('Appearance', back_populates='episode', cascade='all, delete-orphan')
    
    # Limit recursion 
    serialize_rules = ('-guests.episode',)
    
    # validating date
    @validates('date')
    def validate_date(self, key, date):
        if not date or date.strip() == '':
            raise ValueError("Date field must be a string and connot be empty.")
        return date
    
    @validates('number')
    def validate_number(self, key, number):
        if not number or number.strip() == '':
            raise ValueError("Number must be an integer and the filed connot be enmpty.")
        return number
    
    def __repr__(self):
        return f'Episode  {self.number} for date {self.date}'  