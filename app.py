from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv
import uuid
import os
import logging
import traceback

# Configure logging for Vercel
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY') or os.urandom(24)

chatbots = {} # Store the chatbot session instances

@app.route('/')
def home():
    try:
        logger.info("Home route accessed")
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error in home route: {e}")
        logger.error(traceback.format_exc())
        return f"Server is running but encountered an error: {str(e)}", 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'Deep Shiva is running!'})

@app.route('/test')
def test():
    """Simple test endpoint to verify the app is working"""
    try:
        return jsonify({
            'status': 'success',
            'message': 'Flask app is working!',
            'environment': {
                'OPENAI_API_VERSION': bool(os.getenv('OPENAI_API_VERSION')),
                'AZURE_GPT_DEPLOYMENT': bool(os.getenv('AZURE_GPT_DEPLOYMENT')),
                'AZURE_OPENAI_ENDPOINT': bool(os.getenv('AZURE_OPENAI_ENDPOINT')),
                'AZURE_OPENAI_API_KEY': bool(os.getenv('AZURE_OPENAI_API_KEY')),
                'FLASK_SECRET_KEY': bool(os.getenv('FLASK_SECRET_KEY'))
            }
        })
    except Exception as e:
        logger.error(f"Error in test route: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        logger.info("Chat route accessed")
        user_message = request.json.get('message', '')
        persona = request.json.get('persona', None)
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        # For now, return a simple response without chatbot
        response = f"Hello! I received your message: '{user_message}'. The chatbot is currently being initialized."
        
        return jsonify({
            'response': response,
            'has_audio': False
        })
    except Exception as e:
        logger.error(f"Unexpected error in chat: {e}")
        logger.error(traceback.format_exc())
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

@app.route('/clear', methods=['POST'])
def clear_session():
    try:
        session_id = session.get('session_id')
        if session_id and session_id in chatbots:
            chatbots[session_id].clear_memory()
            del chatbots[session_id]
        session.clear()
        return jsonify({'status': 'success'})
    except Exception as e:
        logger.error(f"Error in clear session: {e}")
        return jsonify({'error': str(e)}), 500

# Cleanup function to remove old sessions
def cleanup_old_sessions():
    for session_id in list(chatbots.keys()):
        if session_id not in session:
            del chatbots[session_id]

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 