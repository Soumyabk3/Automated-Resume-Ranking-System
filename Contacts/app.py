from flask import Flask, request, render_template
import os
import PyPDF2

app = Flask(__name__)

# Ensure the uploads folder exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')

def extract_text_from_resume(resume_path):
    """Extract text from a PDF resume."""
    text = ""
    try:
        with open(resume_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error extracting text from {resume_path}: {e}")
    return text.strip()

def calculate_score(resume_text, job_description):
    """Calculate the score based on resume text and job description."""
    matched_words = 0
    total_words = len(job_description.split())  # Total words in job description

    for word in job_description.split():
        if word.lower() in resume_text.lower():
            matched_words += 1  # Increment matched words

    # Calculate the score out of 10
    if total_words > 0:
        score = (matched_words / total_words) * 10
    else:
        score = 0  # In case job description is empty, score is 0

    return round(score, 2), 10  # Return score and max score

@app.route('/')
def index():
    return render_template('index.html', score=None)  # Initially, score is None

@app.route('/upload', methods=['POST'])
def upload():
    if 'resume' not in request.files:
        return 'No resume uploaded.', 400

    resume_file = request.files['resume']
    job_description = request.form['job_description']  # Get the job description

    if resume_file.filename == '':
        return 'No selected file.', 400

    # Save the uploaded resume
    resume_path = os.path.join('uploads', resume_file.filename)
    resume_file.save(resume_path)

    # Extract text from resume
    resume_text = extract_text_from_resume(resume_path)
    print("Extracted Text:", resume_text)  # Check if text is extracted correctly

    # Calculate score using your function
    score, max_score = calculate_score(resume_text, job_description)

    # Pass both score and max score to the template
    return render_template('index.html', score=score, max_score=max_score)

if __name__ == '__main__':
    app.run(debug=True)
