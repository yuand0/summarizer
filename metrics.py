from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from flask import Response

REQUEST_COUNT = Counter(
    'summarize_requests_total',
    'Total summarize requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'summarize_request_duration_seconds',
    'Request latency',
    ['endpoint']
)

CACHE_HIT = Counter('cache_hit_total', 'Cache hits')
CACHE_MISS = Counter('cache_miss_total', 'Cache misses')

def setup_metrics(app):
    @app.route('/metrics')
    def metrics():
        return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)
    return app
