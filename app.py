from flask import Flask, render_template, request, jsonify
import os
import ollama

app = Flask(__name__)

# Conversation history
messages = [{"role": "system", "content": "You are a helpful assistant."}]

# Initialize Ollama client
client = ollama.Client()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    global messages
    user_msg = request.json.get('message', '')
    model = request.json.get('model', 'qwen2.5')  # default model

    if not user_msg.strip():
        return jsonify({'error': 'Empty message'}), 400

    # Add user message to conversation
    messages.append({"role": "user", "content": user_msg})

    # Query Ollama
    try:
        response = client.chat(model=model, messages=messages)
        reply = response["message"]["content"]
    except Exception as e:
        reply = f"Error connecting to Ollama: {str(e)}"

    # Add assistant reply to conversation
    messages.append({"role": "assistant", "content": reply})

    return jsonify({'success': True, 'message': reply})

@app.route('/api/clear', methods=['POST'])
def clear():
    global messages
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
