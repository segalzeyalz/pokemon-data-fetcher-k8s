import requests
import csv
from datetime import datetime

class PokemonService:
    def __init__(self, pokeapi_url, log_file_path, logger):
        self.pokeapi_url = pokeapi_url
        self.log_file_path = log_file_path
        self.logger = logger

    def get_pokemon(self, offset=0, limit=20):
        response = requests.get(f"{self.pokeapi_url}?offset={offset}&limit={limit}")
        if response.status_code != 200:
            raise Exception('Error fetching data from PokeAPI')

        data = response.json()
        pokemons = []
        for item in data['results']:
            pokemon_data = self._fetch_pokemon_data(item['url'])
            pokemons.append(pokemon_data)
        return pokemons

    def _fetch_pokemon_data(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception(f"Error fetching data from {url}")

        data = response.json()
        pokemon_data = {
            'name': data['name'],
            'url': url,
            'hp': data['stats'][0]['base_stat'],
            'attack': data['stats'][1]['base_stat'],
            'defense': data['stats'][2]['base_stat'],
            'special-attack': data['stats'][3]['base_stat'],
            'special-defense': data['stats'][4]['base_stat'],
            'speed': data['stats'][5]['base_stat']
        }
        return pokemon_data

    def log_query(self, params, response):
        try:
            with open(self.log_file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                if file.tell() == 0:
                    # Write header if file is empty
                    writer.writerow(['timestamp', 'params', 'name', 'url', 'hp', 'attack', 'defense', 'special-attack', 'special-defense', 'speed'])
                for pokemon in response:
                    writer.writerow([
                        datetime.now(),
                        params.to_dict(),
                        pokemon['name'],
                        pokemon['url'],
                        pokemon['hp'],
                        pokemon['attack'],
                        pokemon['defense'],
                        pokemon['special-attack'],
                        pokemon['special-defense'],
                        pokemon['speed']
                    ])
        except Exception as e:
            self.logger.error('Error logging query: %s', e)
