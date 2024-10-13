from random import choice as rc
from app import app
from models.guest import Guest
from models.episode import Episode
from models.appearance import Appearance
from sqlalchemy.exc import IntegrityError
from utils.dbconfig import db

if __name__ == '__main__':
    with app.app_context():
        print("Clearing db...")
        Guest.query.delete()
        Episode.query.delete()
        Appearance.query.delete()


        # Create sample guests 
        guests = [
            Guest(name="John Doe", occupation="Actor"),
            Guest(name="Jane Smith", occupation="Musician"),
            Guest(name="Chris Johnson", occupation="Comedian"),
            Guest(name="Emily Clark", occupation="Author"),
            Guest(name="Michael Brown", occupation="Director"),
            Guest(name="Anna Taylor", occupation="Producer"),
            Guest(name="David White", occupation="Singer"),
            Guest(name="Sara Green", occupation="Dancer"),
            Guest(name="Mark Thompson", occupation="Photographer"),
            Guest(name="Sophia Lee", occupation="Influencer")
        ]

        # Create sample episodes
        episodes = [
            Episode(date="2023-01-01", number=1),
            Episode(date="2023-01-02", number=2),
            Episode(date="2023-01-03", number=3),
            Episode(date="2023-01-04", number=4),
            Episode(date="2023-01-05", number=5),
            Episode(date="2023-01-06", number=6),
            Episode(date="2023-01-07", number=7),
            Episode(date="2023-01-08", number=8),
            Episode(date="2023-01-09", number=9),
            Episode(date="2023-01-10", number=10)
        ]

        # Create sample appearances 
        appearances = [
            Appearance(rating=5, guest=guests[0], episode=episodes[0]),
            Appearance(rating=4, guest=guests[1], episode=episodes[1]),
            Appearance(rating=3, guest=guests[2], episode=episodes[2]),
            Appearance(rating=5, guest=guests[3], episode=episodes[3]),
            Appearance(rating=2, guest=guests[4], episode=episodes[4]),
            Appearance(rating=4, guest=guests[5], episode=episodes[5]),
            Appearance(rating=3, guest=guests[6], episode=episodes[6]),
            Appearance(rating=5, guest=guests[7], episode=episodes[7]),
            Appearance(rating=2, guest=guests[8], episode=episodes[8]),
            Appearance(rating=4, guest=guests[9], episode=episodes[9]),
        ]

        try:
            # Add guests and episodes to the session
            db.session.add_all(guests)
            db.session.add_all(episodes)
            db.session.add_all(appearances)

            # Commit the session to save data
            db.session.commit()
            print("Database seeded successfully with 10 guests, 10 episodes, and 10 appearances!")
        except IntegrityError as e:
            db.session.rollback()
            print(f"Error seeding the database: {e}")
