import os
import openai
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')

# Store API usage for analytics
api_calls = []

@app.route('/explain', methods=['POST'])
def explain_code():
    data = request.json
    code = data.get('code', '')
    language = data.get('language', 'unknown')
    
    if not code:
        return jsonify({
            'status': 'error',
            'error': 'Code parameter is required'
        }), 400
    
    prompt = f"""Explain this {language} code in clear, simple terms.
Break it down into:
1. What the code does
2. How it works (step by step)
3. Key concepts used
4. Important notes

Code:
```{language}
{code}
```

Provide a clear explanation:"""
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a code explanation expert. Explain code clearly for developers of all levels."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        explanation = response.choices[0].message.content
        
        # Log the API call
        api_calls.append({
            'timestamp': datetime.now().isoformat(),
            'language': language,
            'code_length': len(code)
        })
        
        return jsonify({
            'status': 'success',
            'explanation': explanation,
            'language': language,
            'code_length': len(code)
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': f'Error: {str(e)}'
        }), 500

@app.route('/optimize', methods=['POST'])
def optimize_code():
    """Suggests optimizations for code"""
    data = request.json
    code = data.get('code', '')
    language = data.get('language', 'unknown')
    
    if not code:
        return jsonify({
            'status': 'error',
            'error': 'Code parameter is required'
        }), 400
    
    prompt = f"""Review this {language} code and suggest optimizations.
Provide:
1. Performance improvements
2. Code quality improvements
3. Best practices
4. Security considerations (if applicable)
5. Refactored code example

Code:
```{language}
{code}
```

Provide practical suggestions:"""
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a code review expert. Provide actionable optimization suggestions."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        suggestions = response.choices[0].message.content
        
        return jsonify({
            'status': 'success',
            'suggestions': suggestions,
            'language': language
        })
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'error': f'Error: {str(e)}'
        }), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get API usage statistics"""
    return jsonify({
        'total_calls': len(api_calls),
        'recent_calls': api_calls[-10:]
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'message': 'Code Explainer API is running'
    })

if __name__ == '__main__':
    app.run(debug=True, port=5004)
