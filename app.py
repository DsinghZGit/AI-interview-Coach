from feedback_generator import generate_feedback, calculate_score
from audio_utils import transcribe_audio
from nlp_utils import analyze_text

if __name__ == "__main__":
    audio_file = "test_audio/sample1.wav"

    try:
        # Step 1: Transcription
        text = transcribe_audio(audio_file)

        # Step 2: NLP Analysis
        analysis = analyze_text(text)

        # Step 3: Generate Feedback & Score
        feedback = generate_feedback(analysis)
        score = calculate_score(analysis)

        # Step 4: Console Output
        print("\n🔊 Transcribed Text:\n", text)
        print("\n🧠 NLP Analysis:")
        print(f"Filler Words: {analysis['filler_words']}")
        print(f"Sentiment: {analysis['sentiment']['tone']} ({analysis['sentiment']['score']:.2f})")
        print(f"Keywords Found: {analysis['keywords_found']}")
        print(f"Keywords Missing: {analysis['keywords_missing']}")
        print("\n💡 Feedback:\n", feedback)
        print(f"\n🎯 Final Score: {score}/100")

        # Step 5: Save to Output File
        with open("output_report.txt", "w") as f:
            f.write("--- Transcription ---\n")
            f.write(text + "\n\n")

            f.write("--- Analysis ---\n")
            f.write(str(analysis) + "\n\n")

            f.write("--- Feedback ---\n")
            f.write(feedback + "\n\n")

            f.write(f"--- Final Score: {score}/100 ---\n")

    except Exception as e:
        print("❌ Something went wrong:", e)
