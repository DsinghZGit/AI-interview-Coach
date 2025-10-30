import gradio as gr
from audio_utils import transcribe_audio
from nlp_utils import analyze_text
from feedback_generator import generate_feedback, calculate_score
import matplotlib.pyplot as plt
from report_generator import save_report_as_pdf
import tempfile
import os



def generate_chart(analysis, score):
    labels = ['Filler Word Penalty', 'Keyword Bonus', 'Sentiment']

    filler_penalty = sum(analysis["filler_words"].values()) * 2
    keyword_bonus = len(analysis["keywords_found"]) * 2
    sentiment_score = 5 if analysis["sentiment"]["tone"] == "Positive" else (-5 if analysis["sentiment"]["tone"] == "Negative" else 0)

    values = [filler_penalty, keyword_bonus, sentiment_score]

    fig, ax = plt.subplots()
    ax.bar(labels, values, color=['red', 'green', 'blue'])
    ax.set_title(f"Score Breakdown (Total: {score}/100)")
    ax.set_ylabel("Points (+/-)")
    return fig


def process_audio(audio):
    print("Audio received:", type(audio))
    try:
        text = transcribe_audio(audio)
        analysis = analyze_text(text)
        feedback = generate_feedback(analysis)
        score = calculate_score(analysis)
        chart = generate_chart(analysis, score)

        # ✅ Insert into MySQL DB
        import mysql.connector
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sqlnew1234",
            database="ai_interview"
        )
        cursor = db.cursor()

        # ✅ Get user_id from username
        username = "dilpreet"  # TEMP hardcoded, later replace with logged-in username
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if user:
            user_id = user[0]
            cursor.execute(
                "INSERT INTO sessions (user_id, score, feedback) VALUES (%s, %s, %s)",
                (user_id, score, feedback)
            )
            db.commit()

        # ✅ Save as PDF
        save_report_as_pdf(text, analysis, feedback, score)

        result = f"""📝 Transcription:\n{text}\n\n
🧠 Sentiment: {analysis['sentiment']['tone']} ({analysis['sentiment']['score']:.2f})\n
💬 Filler Words: {analysis['filler_words']}\n
✅ Keywords Found: {analysis['keywords_found']}\n
❌ Keywords Missing: {analysis['keywords_missing']}\n
💡 Feedback:\n{feedback}\n
🎯 Score: {score}/100
"""

        # Create temporary txt.file to download
        with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as f:
            f.write(result)
            report_path = f.name

        return result, chart, report_path
    except Exception as e:
        return f"❌ Error: {e}", None, None


# Launch Web UI
iface = gr.Interface(
    fn=process_audio,
    inputs=gr.Audio(label="Upload or Record Interview Audio", type="numpy"),
    outputs=["text", "plot", gr.File(label="📥 Download PDF Report")],
    title="🎙️ AI Interview Coach",
    description="Upload your speaking audio and get feedback, score, and a downloadable PDF report."
).launch()



