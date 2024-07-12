from flask import Blueprint, jsonify, request, current_app
from services.pokemon_service import PokemonService
from utils.metrics import pokemon_requests

def create_pokemon_blueprint(pokemon_service):
    pokemon_blueprint = Blueprint('pokemon', __name__)

    @pokemon_blueprint.route('/pokemon', methods=['GET'])
    def get_pokemon():
        """
        Fetches a list of 20 pokemon from the PokeAPI
        :return:
        """
        if pokemon_requests:
            pokemon_requests.inc()

        try:
            pokemon_list = pokemon_service.get_pokemon()
            pokemon_service.log_query(request.args)
            return jsonify(pokemon_list)
        except Exception as e:
            current_app.logger.error('Error fetching data: %s', e)
            return jsonify({'error': 'Failed to fetch data'}), 500

    return pokemon_blueprint
