from flask import Flask, jsonify, request
import requests
import csv
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()
POKEAPI_URL = os.getenv('POKEAPI_URL')
LOG_FILE_PATH = 'queries.csv'

def log_query(query_params):
    file_exists = os.path.isfile(LOG_FILE_PATH)
    with open(LOG_FILE_PATH, 'a', newline='') as csvfile:
        fieldnames = ['query']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()  # file doesn't exist yet, write a header
        writer.writerow({'query': query_params})

@app.route('/pokemon', methods=['GET'])
def get_pokemon():
    """
    Fetches a list of 20 pokemon from the PokeAPI
    :return:
    """
    try:
        response = requests.get(f"{POKEAPI_URL}?limit=20")
        response.raise_for_status()
        data = response.json()
        pokemon_list = []
        for pokemon in data['results']:
            pokemon_data = requests.get(pokemon['url']).json()
            pokemon_list.append({
                'name': pokemon['name'],
                'url': pokemon['url'],
                'stats': {stat['stat']['name']: stat['base_stat'] for stat in pokemon_data['stats']}
            })

        log_query(request.args)
        return jsonify(pokemon_list)
    except requests.exceptions.RequestException as e:
        app.logger.error('Error fetching data: %s', e)
        return jsonify({'error': 'Failed to fetch data'}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
