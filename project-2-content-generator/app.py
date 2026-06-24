import os
import openai
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')

# Define different content generation prompts
CONTENT_PROMPTS = {
    'instagram': 'Generate 3 engaging Instagram captions about "{topic}". Make them catchy and include relevant emojis. Each caption should be 2-3 sentences.',
    'twitter': 'Generate 3 interesting Twitter posts (max 280 characters) about "{topic}". Make them engaging and shareable.',
    'linkedin': 'Generate 3 professional LinkedIn posts about "{topic}". Make them insightful and valuable for professionals.',
    'email': 'Generate 3 catchy email subject lines about "{topic}". Each should be compelling and click-worthy.',
    'blog': 'Generate 3 blog post titles and one-sentence descriptions about "{topic}". Make them SEO-friendly.',
    'youtube': 'Generate 3 YouTube video titles and descriptions about "{topic}". Make them clickable and descriptive.'
}

@app.route('/')
def index():
    return render_template('generator.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    topic = data.get('topic', '')
    content_type = data.get('type', 'instagram')
    
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
    
    if content_type not in CONTENT_PROMPTS:
        return jsonify({'error': 'Invalid content type'}), 400
    
    prompt = CONTENT_PROMPTS[content_type].format(topic=topic)
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a creative content writer. Generate high-quality, engaging content. Return only the content, no explanations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.8,
            max_tokens=1000
        )
        
        generated_content = response.choices[0].message.content
        
        return jsonify({
            'status': 'success',
            'content': generated_content,
            'topic': topic,
            'type': content_type
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Error: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/content-types', methods=['GET'])
def get_content_types():
    return jsonify({
        'types': list(CONTENT_PROMPTS.keys())
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
