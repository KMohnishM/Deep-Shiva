from flask import Flask, render_template, request, jsonify, session
from chatbot import TourismChatbot
from dotenv import load_dotenv
import uuid
import os
import logging

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
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
            try:
                chatbots[session['session_id']] = TourismChatbot()
            except Exception as e:
                logger.error(f"Error creating chatbot on home: {e}")
                # Continue without chatbot for now
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error in home route: {e}")
        return "Server is running but encountered an error. Please check logs.", 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'Deep Shiva is running!'})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        persona = request.json.get('persona', None)
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        session_id = session.get('session_id')
        if not session_id or session_id not in chatbots:
            session['session_id'] = str(uuid.uuid4())
            try:
                chatbots[session['session_id']] = TourismChatbot()
            except Exception as e:
                logger.error(f"Error creating chatbot: {e}")
                return jsonify({'error': 'Failed to initialize chatbot. Please check your Azure OpenAI configuration.'}), 500
            session_id = session['session_id']
        
        chatbot = chatbots[session_id]
        
        # Update persona if changed
        chatbot.set_persona(persona)
        
        # Get response
        try:
            response = chatbot.get_response(user_message)
        except Exception as e:
            logger.error(f"Error getting response: {e}")
            return jsonify({'error': 'Failed to get response from AI. Please try again.'}), 500
        
        # Check if response contains audio markers
        has_audio = '[AUDIO]' in response
        
        return jsonify({
            'response': response,
            'has_audio': has_audio
        })
    except Exception as e:
        logger.error(f"Unexpected error in chat: {e}")
        return jsonify({'error': 'An unexpected error occurred. Please try again.'}), 500

@app.route('/clear', methods=['POST'])
def clear_session():
    session_id = session.get('session_id')
    if session_id and session_id in chatbots:
        chatbots[session_id].clear_memory()
        del chatbots[session_id]
    session.clear()
    return jsonify({'status': 'success'})

# Cleanup function to remove old sessions
def cleanup_old_sessions():
    for session_id in list(chatbots.keys()):
        if session_id not in session:
            del chatbots[session_id]

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 