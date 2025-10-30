from flask import Flask,request,jsonify,render_template
from werkzeug.utils import secure_filename
import os
from audio_utils import transcribe_audio
from nlp_utils import analyze_text
from feedback_generator import generate_feedback, calculate_score
from flask import session


import mysql.connector

app = Flask(__name__)

# To connect with SQL server
db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'Sqlnew1234',
    database = 'ai_interview'
)
cursor = db.cursor()
@app.route('/')
def home():
    return render_template("login.html")
@app.route('/upload')
def upload_form():
    return render_template("upload.html")


app.secret_key = 'a3f2e7c9986c42b1a8d64d4c6df8f4a7'

# For get API
@app.route('/sessions/<username>', methods=['GET'])
def get_sessions(username):
    try:
        # Get user_id
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            return jsonify({"error": "User not found"}), 404

        user_id = user[0]

        # Fetch sessions
        cursor.execute("SELECT date, score, feedback FROM sessions WHERE user_id = %s", (user_id,))
        sessions = cursor.fetchall()

        session_list = [
            {"date": str(row[0]), "score": row[1], "feedback": row[2]}
            for row in sessions
        ]

        return jsonify({"sessions": session_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


### For HTML

@app.route('/dashboard/<username>')
def dashboard(username):
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if not user:
        return "User not found", 404
    user_id = user[0]

    cursor.execute("SELECT date, score, feedback FROM sessions WHERE user_id = %s", (user_id,))
    session_data = cursor.fetchall()

    sessions = [
        {"date": row[0], "score": row[1], "feedback": row[2]}
        for row in session_data
    ]

    return render_template("dashboard.html", username=username, sessions=sessions)



### For get


# @app.route('/sessions/<username>', methods=['GET'])
# def get_user_sessions(username):
#     try:
#         # Step 1: Find user ID
#         cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
#         user = cursor.fetchone()
#         if not user:
#             return jsonify({"error": "User not found"}), 404

#         user_id = user[0]

#         # Step 2: Get all sessions
#         cursor.execute("SELECT date, score, feedback FROM sessions WHERE user_id = %s", (user_id,))
#         sessions = cursor.fetchall()

#         # Step 3: Return as JSON
#         session_list = [
#             {"date": str(row[0]), "score": row[1], "feedback": row[2]}
#             for row in sessions
#         ]
#         return jsonify({"username": username, "sessions": session_list})
    
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500



# @app.route('/add_session', methods=['POST'])
# def add_session():
#     data = request.json
#     username = data['username']
#     score = data['score']
#     feedback = data['feedback']

#     # Get user_id from username
#     cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
#     user = cursor.fetchone()

#     if user:
#         user_id = user[0]
#         cursor.execute(
#             "INSERT INTO sessions (user_id, score, feedback) VALUES (%s, %s, %s)",
#             (user_id, score, feedback)
#         )
#         db.commit()
#         return jsonify({"message": "Session saved successfully"}), 201
#     else:
#         return jsonify({"error": "User not found"}), 404



@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('username')
    password = request.form['password']
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/save-session', methods=['POST'])
def save_session():
    data = request.json
    username = data['username']
    score = data['score']
    feedback = data['feedback']

    try:
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"error":"Not found"}),404

        user_id = user[0]

        #Insert
        cursor.execute(
            "INSERT INTO sessions (user_id, score, feedback) VALUES (%s, %s, %s)",
            (user_id, score, feedback)
        )
        db.commit()
        return jsonify({"message": "Session saved successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/add_session', methods=['POST'])
def add_session():
    data = request.json
    username = data['username']
    score = data['score']
    feedback = data['feedback']

    try:
        # Get user ID for this username
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            user_id = user[0]
            cursor.execute("INSERT INTO sessions (user_id, score, feedback) VALUES (%s, %s, %s)", (user_id, score, feedback))
            db.commit()
            return jsonify({"message": "Session saved successfully"}), 201
        else:
            return jsonify({"error": "User not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



@app.route('/analyze', methods=['POST'])
def analyze_audio():
    if 'audio' not in request.files:
        return "No audio file uploaded", 400

    file = request.files['audio']
    username = request.form.get('username')


    if file.filename == '':
        return "No file selected", 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Step 1: Transcription
    text = transcribe_audio(filepath)

    # Step 2: NLP Analysis
    analysis = analyze_text(text)

    # Step 3: Feedback and Score
    feedback = generate_feedback(analysis)
    score = calculate_score(analysis)

    # Step 4: Save to DB
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    if not user:
        return "User not found", 404

    user_id = user[0]
    cursor.execute("INSERT INTO sessions (user_id, score, feedback) VALUES (%s, %s, %s)",
                   (user_id, score, feedback))
    db.commit()

    # Step 5: Show results
    return render_template("result.html",
                           username=username,
                           text=text,
                           analysis=analysis,
                           feedback=feedback,
                           score=score)

@app.route('/login', methods=['POST'])
@app.route('/signup-page')
def signup_page():
    return render_template("signup.html")

def login():
    username = request.form.get('username')

    password = request.form['password']

    if not username or not password:
        return render_template("login.html")

    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()

    if user:
        # Fetch session data
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        user_id = user[0]

        cursor.execute("SELECT date, score, feedback FROM sessions WHERE user_id = %s", (user_id,))
        session_data = cursor.fetchall()

        sessions = [
            {"date": row[0], "score": row[1], "feedback": row[2]}
            for row in session_data
        ]

        return render_template("dashboard.html", username=username, sessions=sessions)
    else:
        return render_template("login.html", error="Invalid username or password")



if __name__ == "__main__":
    app.run(debug=True)


