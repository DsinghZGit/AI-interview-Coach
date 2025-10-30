from nlp_utils import TECH_KEYWORDS

def generate_feedback(analysis):
    feedback = []

    # Filler Word Feedback
    if analysis["filler_words"]:
        fillers = analysis["filler_words"]
        total = sum(fillers.values())
        feedback.append(f"You used {total} filler words: {', '.join(fillers.keys())}. Try to reduce them.")
    else:
        feedback.append("Great job! You didn’t use any filler words. 👍")

    # Sentiment Feedback
    sentiment = analysis["sentiment"]["tone"]
    if sentiment == "Positive":
        feedback.append("Your tone was confident and positive. Keep it up! ✅")
    elif sentiment == "Negative":
        feedback.append("Your tone seemed negative. Try to sound more confident or enthusiastic.")
    else:
        feedback.append("Your tone was neutral. You can try to add more energy or emotion.")

    # Keyword Feedback
    found = analysis["keywords_found"]
    missing = analysis["keywords_missing"]
    if found:
        feedback.append(f"You mentioned important keywords: {', '.join(found)}.")
    if missing:
        feedback.append(f"You missed these keywords: {', '.join(missing)}. Try to include them next time.")

    return "\n".join(feedback)

def calculate_score(analysis):
    from nlp_utils import TECH_KEYWORDS
    score = 100

    filler_count = sum(analysis["filler_words"].values())
    score -= filler_count * 2  

    tone = analysis["sentiment"]["tone"]
    if tone == "Positive":
        score += 5
    elif tone == "Negative":
        score -= 5

    total_keywords = len(TECH_KEYWORDS)
    found_keywords = len(analysis["keywords_found"])
    
    # Penalty for keyword weakness
    if found_keywords == 0:
        score -= 10
        score = min(score, 0)  # Strong cap
    elif found_keywords < total_keywords / 2:
        score -= 5

    score += found_keywords * 2

    score = max(0, min(100, score))
    return score


       


    