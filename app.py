from flask import Flask, jsonify, request
from response import success, error
from summarize import generate_summary

def create_app():
    app = Flask(__name__)

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

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
