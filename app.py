from flask import Flask
from config import Config
from controllers.pokemon_controller import create_pokemon_blueprint
from utils.logging import setup_logging
from utils.metrics import setup_metrics
from utils.tracing import setup_tracing
from services.pokemon_service import PokemonService

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Setup logging
    setup_logging(app)

    # Setup metrics
    setup_metrics(app)

    # Setup tracing
    setup_tracing(app)

    # Initialize the PokemonService with app config and logger
    pokemon_service = PokemonService(app.config['POKEAPI_URL'], app.config['LOG_FILE_PATH'], app.logger)

    # Register blueprints
    app.register_blueprint(create_pokemon_blueprint(pokemon_service))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.config['DEBUG'], host="0.0.0.0", port=5000)
