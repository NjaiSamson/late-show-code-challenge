from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

# imports db configaration from utils folder
from utils.dbconfig import db

class Appearance(db.Model, SerializerMixin):
    __tablename__ = 'appearances'
    
    # Limiting recursion 
    serialize_rules = ('-hero.powers', '-power.heroes')
    
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    
    # ForeignKey stores guest id and episode id
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)
    
    # Relationship mapping the episode to the related guest
    guest = db.relationship('Guest', back_populates="episodes")
    episode = db.relationship('Episode', back_populates="guests")
    
    # validating ratings
    @validates('rating')
    def validate_strength_field(self, key, rating):
        allowed_rating = [1,2,3,4,5]
        if not rating or rating.strip() == '':
            raise ValueError("Ratings can not be empty")
        
        if not any(rate in rating for rate in allowed_rating):
            raise ValueError("That value rating is not allowed")
    
    def __repr__(self):
        return f'Guest rating {self.rating} rate id {self.id}'  