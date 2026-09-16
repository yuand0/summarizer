import logging
import uuid
from flask import request, g

class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = getattr(g, 'request_id', 'N/A')
        return True

def setup_logging(app):
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(asctime)s - [%(request_id)s] - %(levelname)s - %(message)s'
    ))
    handler.addFilter(RequestIdFilter())

    app.logger.handlers = [handler]
    app.logger.setLevel(logging.INFO)

    @app.before_request
    def before_request():
        g.request_id = request.headers.get('X-Request-ID', str(uuid.uuid4())[:8])

    @app.after_request
    def after_request(response):
        response.headers['X-Request-ID'] = g.get('request_id', '')
        return response

    return app
