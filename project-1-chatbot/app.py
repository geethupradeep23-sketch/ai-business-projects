import os
import openai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')

# Customize this for different bot personalities
SYSTEM_PROMPT = "You are a helpful, friendly AI assistant. Be concise and helpful in your responses."

# Store conversation history
conversation_history = []

@app.route('/')
def index():
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400
    
    # Add user message to history
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    try:
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT}
            ] + conversation_history,
            temperature=0.7,
            max_tokens=500
        )
        
        assistant_message = response.choices[0].message.content
        
        # Add assistant response to history
        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return jsonify({
            'response': assistant_message,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Error: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/reset', methods=['POST'])
def reset():
    global conversation_history
    conversation_history = []
    return jsonify({'status': 'success', 'message': 'Conversation reset'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
