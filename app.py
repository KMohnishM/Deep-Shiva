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

# Import chatbot with error handling
try:
    from chatbot import TourismChatbot
    CHATBOT_AVAILABLE = True
    logger.info("Chatbot module imported successfully")
except Exception as e:
    CHATBOT_AVAILABLE = False
    logger.error(f"Failed to import chatbot: {e}")
    logger.error(traceback.format_exc())

@app.route('/')
def home():
    try:
        logger.info("Home route accessed")
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error in home route: {e}")
        logger.error(traceback.format_exc())
        # Return a simple HTML response if template fails
        return f'''
        <!DOCTYPE html>
        <html>
        <head><title>Deep Shiva - Error</title></head>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>🧘‍♀️ Deep Shiva</h1>
            <p>Server is running but encountered an error: {str(e)}</p>
            <p>Please check the logs for more details.</p>
        </body>
        </html>
        ''', 500

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
            'chatbot_available': CHATBOT_AVAILABLE,
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

        if not CHATBOT_AVAILABLE:
            return jsonify({
                'response': "I'm sorry, the AI chatbot is currently unavailable. Please try again later.",
                'has_audio': False
            })

        session_id = session.get('session_id')
        if not session_id or session_id not in chatbots:
            session['session_id'] = str(uuid.uuid4())
            try:
                chatbots[session['session_id']] = TourismChatbot()
                logger.info("Chatbot created successfully")
            except Exception as e:
                logger.error(f"Error creating chatbot: {e}")
                logger.error(traceback.format_exc())
                return jsonify({'error': 'Failed to initialize chatbot. Please check your Azure OpenAI configuration.'}), 500
            session_id = session['session_id']
        
        chatbot = chatbots[session_id]
        
        # Update persona if changed
        chatbot.set_persona(persona)
        
        # Get response
        try:
            response = chatbot.get_response(user_message)
            logger.info("Response generated successfully")
        except Exception as e:
            logger.error(f"Error getting response: {e}")
            logger.error(traceback.format_exc())
            return jsonify({'error': 'Failed to get response from AI. Please try again.'}), 500
        
        # Check if response contains audio markers
        has_audio = '[AUDIO]' in response
        
        return jsonify({
            'response': response,
            'has_audio': has_audio
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