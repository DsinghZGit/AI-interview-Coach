
🎤 AI Interview Coach
🚀 Overview

AI Interview Coach is an intelligent web application that helps users practice and improve their interview skills using speech analysis, NLP, and feedback scoring.
It allows users to record or upload their interview answers and receive detailed feedback on communication, tone, filler words, confidence, and content relevance — just like a real interviewer would!

 Features

 Speech-to-Text (Whisper Integration): Converts spoken answers into text using OpenAI Whisper.

 NLP Analysis: Analyzes transcribed text for tone, confidence, filler words, and relevance.

 Feedback and Scoring System: Provides overall feedback with a numeric score for performance evaluation.

 Result Dashboard: Displays user history, uploaded audio, and performance insights.

 User Authentication: Login, signup, and session tracking using Flask + MySQL.

 Beautiful UI: Clean and responsive Bootstrap dashboard for easy navigation.

 Tech Stack
Component	Technology
Frontend	HTML, CSS, Bootstrap
Backend	Flask (Python)
Database	MySQL
Speech Recognition	OpenAI Whisper
NLP Analysis	Python (NLTK / TextBlob)
UI Integration	Flask Templates + Bootstrap
📂 Project Structure
AI-Interview-Coach/
│
├── auth_app.py           # Flask backend: authentication, sessions, routes
├── audio_utils.py        # Whisper transcription and analysis
├── static/               # CSS, JS, images
├── templates/            # HTML templates (login, signup, dashboard, result)
├── uploads/              # Uploaded audio files
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation

⚙️ Installation & Setup

Clone the repository

git clone https://github.com/yourusername/AI-Interview-Coach.git
cd AI-Interview-Coach


Create and activate virtual environment

python -m venv venv
source venv/bin/activate     # for Mac/Linux
venv\Scripts\activate        # for Windows


Install dependencies

pip install -r requirements.txt


Set up MySQL database

Create a database named ai_interview_db.

Import or create the users table with columns:
id, username, password, session_token.

Run the application

python auth_app.py


Then open your browser at http://localhost: XXXX

 How It Works

Login or Signup to access your dashboard.

Upload your interview audio or record it directly.

The system uses Whisper to transcribe speech into text.

The NLP engine analyzes tone, filler words, keywords, and fluency.

You receive a detailed feedback report and score displayed on the dashboard.

📈 Future Enhancements

 Add real-time voice feedback during mock interviews

 Add AI-generated follow-up questions

 Personalized progress tracking per user

 Integration with job-specific question sets

 Screenshots

<img width="2047" height="1138" alt="image" src="https://github.com/user-attachments/assets/d498eef2-2029-4870-bb42-0966fec2f0e2" />
<img width="2047" height="1161" alt="image" src="https://github.com/user-attachments/assets/579163d7-a86d-4537-95dd-a0f183403143" />



 Author

Dilpreet Singh
