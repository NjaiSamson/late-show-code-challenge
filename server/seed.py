from app import app
from models.guest import Guest
from models.episode import Episode
from models.appearance import Appearance
from utils.dbconfig import db

if __name__ == '__main__':
    with app.app_context():
        print("Clearing db...")
        # Clear the tables
        Episode.query.delete()
        Guest.query.delete()        
        Appearance.query.delete()
        db.create_all()        
        
        # Create sample episodes
        episode1 = Episode(date="2023-01-01", number=1)
        episode2 = Episode(date="2023-01-02", number=2)
        episode3 = Episode(date="2023-01-03", number=3)
        episode4 = Episode(date="2023-01-04", number=4)
        episode5 = Episode(date="2023-01-05", number=5)

        # Create sample guests
        guest1 = Guest(name="John Mwangi", occupation="Actor")
        guest2 = Guest(name="Jane Achieng", occupation="Musician")
        guest3 = Guest(name="Chris Mutua", occupation="Comedian")
        guest4 = Guest(name="Emily Chebet", occupation="Author")
        guest5 = Guest(name="Michael Juma", occupation="Director")
        guest6 = Guest(name="Anna Muteti", occupation="Producer")
        guest7 = Guest(name="David Mutisya", occupation="Singer")
        guest8 = Guest(name="Sara Wairimu", occupation="Dancer")
        guest9 = Guest(name="Mark Silisya", occupation="Photographer")
        guest10 = Guest(name="Sophia Mutheu", occupation="Influencer")

        db.session.add_all([
            episode1, episode2, episode3, episode4, episode5,
            guest1, guest2, guest3, guest4, guest5,
            guest6, guest7, guest8, guest9, guest10
        ])
        db.session.commit()

        # Create sample appearances
        appearance1 = Appearance(episode_id=episode1.id, guest_id=guest1.id, rating=5)
        appearance2 = Appearance(episode_id=episode2.id, guest_id=guest2.id, rating=4)
        appearance3 = Appearance(episode_id=episode3.id, guest_id=guest3.id, rating=3)
        appearance4 = Appearance(episode_id=episode1.id, guest_id=guest4.id, rating=5)
        appearance5 = Appearance(episode_id=episode2.id, guest_id=guest5.id, rating=4)
        appearance6 = Appearance(episode_id=episode4.id, guest_id=guest6.id, rating=2)
        appearance7 = Appearance(episode_id=episode5.id, guest_id=guest7.id, rating=3)
        appearance8 = Appearance(episode_id=episode3.id, guest_id=guest8.id, rating=4)
        appearance9 = Appearance(episode_id=episode4.id, guest_id=guest9.id, rating=5)
        appearance10 = Appearance(episode_id=episode5.id, guest_id=guest10.id, rating=3)
        appearance11 = Appearance(episode_id=episode1.id, guest_id=guest10.id, rating=2)
        appearance12 = Appearance(episode_id=episode3.id, guest_id=guest1.id, rating=5)
        appearance13 = Appearance(episode_id=episode4.id, guest_id=guest5.id, rating=3)
        appearance14 = Appearance(episode_id=episode5.id, guest_id=guest4.id, rating=4)
        appearance15 = Appearance(episode_id=episode2.id, guest_id=guest9.id, rating=5)
    
        print("Seeding the database...")
        db.session.add_all([
            appearance1, appearance2, appearance3, appearance4, appearance5, 
            appearance6, appearance7, appearance8, appearance9, appearance10,
            appearance11, appearance12, appearance13, appearance14, appearance15
        ])
        db.session.commit()
        print("Database seeded successfully!")
