import requests
import csv
import os
import concurrent.futures

class PokemonService:
    def __init__(self, pokeapi_url, log_file_path, logger):
        self.pokeapi_url = pokeapi_url
        self.log_file_path = log_file_path
        self.logger = logger

    def log_query(self, query_params):
        file_exists = os.path.isfile(self.log_file_path)
        with open(self.log_file_path, 'a', newline='') as csvfile:
            fieldnames = ['query']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()  # file doesn't exist yet, write a header
            writer.writerow({'query': str(query_params.to_dict())})

    def fetch_pokemon_data(self, pokemon):
        try:
            pokemon_data = requests.get(pokemon['url']).json()
            return {
                'name': pokemon['name'],
                'url': pokemon['url'],
                'stats': {stat['stat']['name']: stat['base_stat'] for stat in pokemon_data['stats']}
            }
        except requests.exceptions.RequestException as e:
            self.logger.error('Error fetching data for %s: %s', pokemon['name'], e)
            return None

    def get_pokemon(self):
        response = requests.get(f"{self.pokeapi_url}?limit=20")
        response.raise_for_status()
        data = response.json()

        with concurrent.futures.ThreadPoolExecutor() as executor:
            pokemon_list = list(executor.map(self.fetch_pokemon_data, data['results']))

        # Remove any None values in case of request failures
        return [pokemon for pokemon in pokemon_list if pokemon is not None]
