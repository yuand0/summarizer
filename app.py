from flask import Flask, jsonify, request, g
from response import success, error
from summarize import generate_summary
from cache import get_cache_stats
from logging_config import setup_logging
from metrics import setup_metrics, REQUEST_COUNT, REQUEST_LATENCY
import logging
import time

def create_app():
    app = Flask(__name__)
    setup_logging(app)
    setup_metrics(app)

    logger = logging.getLogger(__name__)

    @app.before_request
    def start_timer():
        g.start_time = time.time()

    @app.after_request
    def record_metrics(response):
        if request.path != '/metrics':
            duration = time.time() - g.get('start_time', time.time())
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.path,
                status=response.status_code
            ).inc()
            REQUEST_LATENCY.labels(endpoint=request.path).observe(duration)
        return response

    @app.route('/')
    def index():
        return jsonify(success({"project": "summarizer", "version": "0.1.0"}))

    @app.route('/health')
    def health():
        return jsonify(success())

    @app.route('/summarize', methods=['POST'])
    def summarize():
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify(error(400, "缺少 text 字段")), 400
        
        text = data['text']
        max_length = data.get('max_length', 100)
        
        result = generate_summary(text, max_length)
        if 'error' in result:
            return jsonify(error(400, result['error'])), 400
        
        return jsonify(success(result))

    @app.route('/cache/stats')
    def cache_stats():
        return jsonify(success(get_cache_stats()))

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
