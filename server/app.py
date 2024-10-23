from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
from flask_migrate import Migrate

# models importations
from models.guest import Guest
from models.episode import Episode
from models.appearance import Appearance

# db configuration importation
from utils.dbconfig import db

# Configuring the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True 

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

# Homepage route
class Index(Resource):
    def get(self):
        response_dict = {"message": "Welcome to the Late Show API",}
        response = make_response(response_dict, 200)
        return response
api.add_resource(Index, '/')

class Episodes(Resource):
    # Getting episodes
    def get(self):
        episode_list = Episode.query.all()
        return make_response(jsonify([episode.to_dict() for episode in episode_list]))

api.add_resource(Episodes, '/episodes')


class EpisodeByID(Resource):
    def get(self, id):
        episode_by_id = Episode.query.get(id)
        if not episode_by_id:
            return make_response(jsonify({"error": "Episode not found"}), 404)
        else:
            # Return episode information along with guests
            return make_response(jsonify(episode_by_id.to_dict(guests_appeared=True)), 200)
    
    def delete(self, id):
        # Fetch the episode by its id
        episode = Episode.query.filter_by(id=id).first()

        if not episode:
            return make_response(jsonify({"errors": ["Episode not found"]}), 404)

        try:
            # Delete the episode 
            db.session.delete(episode)
            db.session.commit()
            return make_response(jsonify({"message": "Episode deleted successfully"}), 200)

        except Exception as e:
            db.session.rollback()  
            return make_response(jsonify({"errors": [str(e)]}), 500)

api.add_resource(EpisodeByID, '/episodes/<int:id>')


# Guests route
class Guests(Resource):
    # Getting guests
    def get(self):
        guest_list = Guest.query.all()
        return make_response(jsonify([guest.to_dict() for guest in guest_list]), 200)

api.add_resource(Guests, '/guests')

# Appearance posting route
class Appearances(Resource):
    def post(self):
        try:
            # Collecting data from the JSON body
            data = request.get_json()

            rating = data.get('rating')
            guest_id = data.get('guest_id')
            episode_id = data.get('episode_id')

            # Validate required fields
            if rating is None or guest_id is None or episode_id is None:
                return make_response(jsonify({"errors": ["Required field missing"]}), 400)

            # Convert guest_id, episode_id, and rating to integers
            try:
                rating = int(rating)
                guest_id = int(guest_id)
                episode_id = int(episode_id)
            except ValueError:
                return make_response(jsonify({"errors": ["guest_id, episode_id, and rating must be integers"]}), 400)

            # Validate rating before checking for duplicates
            if rating < 1 or rating > 5:
                return make_response(jsonify({"errors": ["Rating must be between 1 and 5"]}), 400)

            # Fetch episode and guest from the database
            episode = Episode.query.filter_by(id=episode_id).first()
            guest = Guest.query.filter_by(id=guest_id).first()

            if not episode:
                return make_response(jsonify({"errors": ["Episode not found"]}), 404)
            if not guest:
                return make_response(jsonify({"errors": ["Guest not found"]}), 404)

            # Checking for duplicates
            duplicate_appearance = Appearance.query.filter_by(guest_id=guest_id, episode_id=episode_id).first()
            if duplicate_appearance:
                return make_response(jsonify({"errors": ["Duplicate appearance for this guest and episode on this date. Note that a guest can appear only once for a given episode at a particular date."]}), 400)

            # Create a new Appearance record
            new_appearance = Appearance(
                rating=rating,
                guest_id=guest_id,
                episode_id=episode_id
            )
            db.session.add(new_appearance)
            db.session.commit()

            # Response data
            response_data = {
                "id": new_appearance.id,
                "rating": new_appearance.rating,
                "guest_id": guest.id,
                "episode_id": episode.id,
                "episode": {
                    "date": episode.date,
                    "id": episode.id,
                    "number": episode.number
                },
                "guest": {
                    "id": guest.id,
                    "name": guest.name,
                    "occupation": guest.occupation
                }
            }
            return make_response(jsonify(response_data), 201)

        # Handle validation errors
        except ValueError as e:            
            return make_response(jsonify({"errors": [str(e)]}), 400)

        except Exception as e:
            return make_response(jsonify({"errors": [str(e)]}), 500)

api.add_resource(Appearances, '/appearances')


if __name__ == '__main__':
    app.run(port=5555, debug=True)