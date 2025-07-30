from flask import Flask, render_template, request, jsonify, session
from chatbot import TourismChatbot
from dotenv import load_dotenv
import uuid
import os
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY') or os.urandom(24)

chatbots = {} # Store the chatbot session instances

@app.route('/')
def home():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        chatbots[session['session_id']] = TourismChatbot()
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    persona = request.json.get('persona', None)
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    session_id = session.get('session_id')
    if not session_id or session_id not in chatbots:
        session['session_id'] = str(uuid.uuid4())
        chatbots[session['session_id']] = TourismChatbot()
        session_id = session['session_id']
    
    chatbot = chatbots[session_id]
    
    # Update persona if changed
    chatbot.set_persona(persona)
    
    # Get response
    response = chatbot.get_response(user_message)
    
    # Check if response contains audio markers
    has_audio = '[AUDIO]' in response
    
    return jsonify({
        'response': response,
        'has_audio': has_audio
    })

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