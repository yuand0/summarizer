from flask import Flask, jsonify, request, g
from response import success, error
from summarize import generate_summary
from cache import get_cache_stats
from logging_config import setup_logging
import logging
import uuid

def create_app():
    app = Flask(__name__)
    setup_logging(app)

    logger = logging.getLogger(__name__)

    @app.route('/')
    def index():
        return jsonify(success({"project": "summarizer", "version": "0.1.0"}))

    @app.route('/health')
    def health():
        return jsonify(success())

    @app.route('/summarize', methods=['POST'])
    def summarize():
        request_id = g.get('request_id', 'unknown')
        logger.info(f"收到摘要请求, request_id={request_id}")
        
        data = request.get_json()
        if not data or 'text' not in data:
            logger.warning(f"缺少 text 字段, request_id={request_id}")
            return jsonify(error(400, "缺少 text 字段")), 400
        
        text = data['text']
        max_length = data.get('max_length', 100)
        
        result = generate_summary(text, max_length)
        if 'error' in result:
            logger.error(f"摘要失败: {result['error']}, request_id={request_id}")
            return jsonify(error(400, result['error'])), 400
        
        logger.info(f"摘要成功, request_id={request_id}")
        return jsonify(success(result))

    @app.route('/cache/stats')
    def cache_stats():
        return jsonify(success(get_cache_stats()))

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
