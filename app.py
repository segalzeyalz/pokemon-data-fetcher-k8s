from flask import Flask, jsonify, request
import requests
import csv
import os
from dotenv import load_dotenv
import concurrent.futures
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
metrics = PrometheusMetrics(app)

# Define custom metrics
pokemon_requests = metrics.counter(
    'pokemon_requests_total', 'Number of requests to the /pokemon endpoint'
)
# app.py - Example addition for Prometheus metrics
from prometheus_flask_exporter import PrometheusMetrics
metrics = PrometheusMetrics(app)

# Flask route to expose metrics
@app.route('/metrics')
def metrics():
    return metrics.generate_latest()


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
        writer.writerow({'query': str(query_params)})

@pokemon_requests.count_exceptions()
def fetch_pokemon_data(pokemon):
    try:
        pokemon_data = requests.get(pokemon['url']).json()
        return {
            'name': pokemon['name'],
            'url': pokemon['url'],
            'stats': {stat['stat']['name']: stat['base_stat'] for stat in pokemon_data['stats']}
        }
    except requests.exceptions.RequestException as e:
        app.logger.error('Error fetching data for %s: %s', pokemon['name'], e)
        return None

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

        with concurrent.futures.ThreadPoolExecutor() as executor:
            pokemon_list = list(executor.map(fetch_pokemon_data, data['results']))

        # Remove any None values in case of request failures
        pokemon_list = [pokemon for pokemon in pokemon_list if pokemon is not None]

        log_query(request.args)
        return jsonify(pokemon_list)
    except requests.exceptions.RequestException as e:
        app.logger.error('Error fetching data: %s', e)
        return jsonify({'error': 'Failed to fetch data'}), 500

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
