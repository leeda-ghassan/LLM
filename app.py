from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

# Conversation history
messages = []

# LLM Configuration
LLM_MODEL = "qwen2.5"   # MUST match installed model name
OLLAMA_URL = "http://ollama:11434"   # Use Docker service name


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "").strip()
    if not user_msg:
        return jsonify({"error": "Empty message"}), 400

    messages.append({"role": "user", "content": user_msg})
    
    response = get_llm_response(user_msg)

    messages.append({"role": "assistant", "content": response})
    return jsonify({"success": True, "message": response})


def get_llm_response(user_input):
    """
    Sends user input to Ollama using /api/chat (non-streaming).
    """
    try:
        payload = {
            "model": LLM_MODEL,
            "messages": [
                {"role": "user", "content": user_input}
            ],
            "stream": False  # IMPORTANT: disables streaming
        }

        res = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=30)
        res.raise_for_status()

        data = res.json()

        # Extract assistant reply
        return data["message"]["content"]

    except Exception as e:
        return f"Error connecting to Ollama: {e}"


    except Exception as e:
        return f"Error connecting to Ollama: {e}"


@app.route("/api/clear", methods=["POST"])
def clear():
    global messages
    messages = []
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5001)
