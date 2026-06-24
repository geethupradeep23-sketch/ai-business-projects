import os
import openai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def index():
    return render_template('resumegen.html')

@app.route('/generate-resume', methods=['POST'])
def generate_resume():
    data = request.json
    
    user_info = f"""Full Name: {data.get('name', '')}
Email: {data.get('email', '')}
Phone: {data.get('phone', '')}
Location: {data.get('location', '')}

Professional Summary: {data.get('summary', '')}

Experience:
{data.get('experience', '')}

Education:
{data.get('education', '')}

Skills:
{data.get('skills', '')}

Target Job Title: {data.get('jobTitle', '')}
Target Company: {data.get('company', '')}
Job Description: {data.get('jobDesc', '')}
"""
    
    prompt = f"""Based on this information, generate a professional, ATS-friendly resume. 
Make it tailored for the target job. Use proper resume formatting with clear sections. 
Highlight relevant skills and experience for the target position.

{user_info}

Generate the resume content (not markdown, just plain formatted text):"""
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional resume writer. Create compelling, ATS-optimized resumes that highlight the candidate's strengths."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        resume = response.choices[0].message.content
        
        return jsonify({
            'status': 'success',
            'resume': resume
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Error: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/generate-cover-letter', methods=['POST'])
def generate_cover_letter():
    data = request.json
    
    user_info = f"""Candidate Name: {data.get('name', '')}
Target Company: {data.get('company', '')}
Target Job Title: {data.get('jobTitle', '')}
Years of Experience: {data.get('experience', '')}

Key Achievements: {data.get('achievements', '')}
Why interested in this company: {data.get('whyCompany', '')}
Key Skills: {data.get('skills', '')}
"""
    
    prompt = f"""Generate a compelling, professional cover letter based on this information. 
Make it personalized and compelling. Show enthusiasm and relevant skills.

{user_info}

Generate the cover letter:"""
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert cover letter writer. Create compelling, professional cover letters that get attention."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        cover_letter = response.choices[0].message.content
        
        return jsonify({
            'status': 'success',
            'coverLetter': cover_letter
        })
    
    except Exception as e:
        return jsonify({
            'error': f'Error: {str(e)}',
            'status': 'error'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5003)
