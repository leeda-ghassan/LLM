from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Simple conversation history
messages = []

# LLM Configuration (for AI)
LLM_API_KEY = os.getenv('LLM_API_KEY', '')
LLM_MODEL = os.getenv('LLM_MODEL', 'gpt-3.5-turbo')  # Change this to your LLM
USE_LLM = os.getenv('USE_LLM', 'False') == 'True'  # Set to True when ready

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message', '')
    
    if not user_input.strip():
        return jsonify({'error': 'Empty message'}), 400
    
    # Add user message to the conversation history
    messages.append({'role': 'user', 'content': user_input})
    
    # Checking if the LLM is configured
    if USE_LLM and LLM_API_KEY:
        response = get_llm_response(user_input)
    else:
        response = "Waiting for LLM integration..."
    
    # AI response if the configuration is done correctly
    messages.append({'role': 'assistant', 'content': response})
    
    #Success response with the AI's response
    return jsonify({'success': True, 'message': response})

def get_llm_response(user_input):
    """
    LLM integration logic goes here.
    """
    return "LLM not configured yet. Please implement the get_llm_response() function." # Placeholder response

#resetting the messages list
@app.route('/api/clear', methods=['POST'])
def clear():
    global messages
    messages = []
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, port=5000)