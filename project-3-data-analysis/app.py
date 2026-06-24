import os
import openai
import pandas as pd
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')

ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls'}
UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('analyzer.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed. Use CSV or Excel files.'}), 400
    
    try:
        # Read the file
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        
        # Generate statistics
        stats = {
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': list(df.columns),
            'data_types': df.dtypes.to_dict(),
            'summary': df.describe().to_dict()
        }
        
        # Create a prompt for OpenAI
        df_summary = f"""Dataset Summary:
- Total Rows: {stats['rows']}
- Total Columns: {stats['columns']}
- Column Names: {', '.join(stats['column_names'])}

First few rows:
{df.head(10).to_string()}

Basic Statistics:
{df.describe().to_string()}
"""
        
        prompt = f"""Analyze this business data and provide:
1. Key insights (3-5 most important findings)
2. Trends or patterns
3. Actionable recommendations for improvement
4. Potential opportunities
5. Any concerns or red flags

{df_summary}

Provide practical, business-focused insights."""
        
        # Get AI analysis
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a business data analyst. Provide clear, actionable insights from data analysis."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        analysis = response.choices[0].message.content
        
        return jsonify({
            'status': 'success',
            'stats': stats,
            'analysis': analysis,
            'filename': secure_filename(file.filename)
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Error analyzing file: {str(e)}',
            'status': 'error'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5002)
