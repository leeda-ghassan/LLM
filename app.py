from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

# Ollama Configuration
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://ollama:11434')
DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'qwen2.5:3b')

# Simple conversation history
conversation_history = []

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages and get AI responses"""
    try:
        data = request.json
        user_msg = data.get('message', '').strip()
        model_choice = data.get('model', 'qwen')  # Get model from frontend
        
        if not user_msg:
            return jsonify({'success': False, 'error': 'Empty message'}), 400
        
        # Choose model based on selection
        if model_choice == "ollama":
            model = "llama3.2:1b"
        else:
            model = "qwen2.5:3b"
        
        # Add user message to history
        conversation_history.append({'role': 'user', 'content': user_msg})
        
        # Get response from Ollama Docker service
        ai_response = get_ollama_response(user_msg, model)
        
        # Add AI response to history
        conversation_history.append({'role': 'assistant', 'content': ai_response})
        
        return jsonify({
            'success': True, 
            'message': ai_response,
            'model_used': model
        })
    
    except Exception as e:
        return jsonify({
            'success': False, 
            'error': f'Server error: {str(e)}'
        }), 500

def get_ollama_response(user_input, model="qwen2.5:3b"):
    """
    Get response from Ollama Docker service
    """
    try:
        # Send request to Ollama
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": model,
                "prompt": user_input,
                "stream": False
            },
            timeout=60  # 60 second timeout for AI responses
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get('response', 'No response received from AI')
        else:
            return f"Error: Ollama service returned status {response.status_code}. Please check if Ollama container is running."
            
    except requests.exceptions.ConnectionError:
        return "Error: Cannot connect to Ollama service. Make sure the Ollama Docker container is running and accessible."
    except requests.exceptions.Timeout:
        return "Error: Request timed out. The AI is taking too long to respond. Please try again."
    except Exception as e:
        return f"Error communicating with AI service: {str(e)}"

@app.route('/api/clear', methods=['POST'])
def clear_chat():
    """Clear conversation history"""
    global conversation_history
    conversation_history = []
    return jsonify({'success': True, 'message': 'Chat history cleared'})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Check if Ollama service is healthy"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            return jsonify({
                'status': 'healthy',
                'ollama_service': 'running',
                'models_available': True
            })
        else:
            return jsonify({
                'status': 'unhealthy', 
                'ollama_service': 'not responding properly',
                'models_available': False
            }), 503
    except Exception as e:
        return jsonify({
            'status': 'unavailable',
            'ollama_service': 'not reachable',
            'error': str(e),
            'models_available': False
        }), 503

@app.route('/api/models', methods=['GET'])
def list_models():
    """List available models in Ollama"""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            models_data = response.json()
            return jsonify({
                'success': True,
                'models': models_data.get('models', [])
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Could not fetch models list'
            }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error fetching models: {str(e)}'
        }), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get conversation history"""
    return jsonify({
        'success': True,
        'history': conversation_history,
        'total_messages': len(conversation_history)
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)