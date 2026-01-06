from flask import Flask, render_template, request, jsonify, session
from chatbot import MedicalChatbot
import os
from datetime import timedelta

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)

# Initialize chatbot (will be loaded per session)
chatbot_instances = {}


def get_chatbot_for_session():
    """Get or create chatbot instance for current session"""
    session_id = session.get('session_id')

    if not session_id:
        # Generate new session ID
        import uuid
        session_id = str(uuid.uuid4())
        session['session_id'] = session_id
        session.permanent = True

    if session_id not in chatbot_instances:
        chatbot_instances[session_id] = MedicalChatbot()

    return chatbot_instances[session_id]


@app.route('/')
def index():
    """Render main chatbot interface"""
    return render_template('index.html')


@app.route('/api/disclaimer', methods=['GET'])
def get_disclaimer():
    """Get medical disclaimer"""
    chatbot = get_chatbot_for_session()
    return jsonify({
        'disclaimer': chatbot.get_disclaimer()
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """Process chat message"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({
                'error': 'No message provided'
            }), 400

        chatbot = get_chatbot_for_session()
        response = chatbot.process_message(user_message)

        return jsonify({
            'response': response,
            'symptoms': chatbot.conversation_state['symptoms'],
            'stage': chatbot.conversation_state['stage']
        })

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/reset', methods=['POST'])
def reset():
    """Reset conversation"""
    try:
        chatbot = get_chatbot_for_session()
        chatbot.reset_conversation()

        return jsonify({
            'message': 'Conversation reset successfully'
        })

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/symptoms', methods=['GET'])
def get_symptoms():
    """Get current symptoms in conversation"""
    try:
        chatbot = get_chatbot_for_session()
        return jsonify({
            'symptoms': chatbot.conversation_state['symptoms'],
            'stage': chatbot.conversation_state['stage']
        })

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Medical Symptom Checker Chatbot',
        'version': '1.0.0'
    })


if __name__ == '__main__':
    # Ensure model is trained before starting
    import os
    if not os.path.exists('models/disease_model.pkl'):
        print("\n" + "="*60)
        print("ERROR: Model not found!")
        print("="*60)
        print("\nPlease run the following commands first:")
        print("1. python generate_dataset.py  # Generate dataset")
        print("2. python train_model.py       # Train model")
        print("\nThen run this application again.")
        print("="*60 + "\n")
    else:
        print("\n" + "="*60)
        print("Medical Symptom Checker Chatbot")
        print("="*60)
        print("\nStarting Flask application...")
        print("Open your browser and navigate to: http://localhost:5000")
        print("\nPress CTRL+C to stop the server.")
        print("="*60 + "\n")

        app.run(debug=True, host='0.0.0.0', port=5000)
