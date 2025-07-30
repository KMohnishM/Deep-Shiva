from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        'message': 'Deep Shiva is running!',
        'status': 'success'
    })

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'message': 'Server is working!'
    })

@app.route('/test')
def test():
    return jsonify({
        'status': 'success',
        'message': 'Minimal app is working!'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 