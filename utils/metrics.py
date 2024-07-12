from prometheus_flask_exporter import PrometheusMetrics

metrics = None
pokemon_requests = None

def setup_metrics(app):
    global metrics, pokemon_requests
    metrics = PrometheusMetrics(app)
    pokemon_requests = metrics.counter(
        'pokemon_requests_total', 'Number of requests to the /pokemon endpoint'
    )
