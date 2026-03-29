def calculate_ats_score(skills, text):

    text = text.lower()
    score = 0

    score += min(len(skills) * 4, 40)

    if "project" in text:
        score += 15

    if "experience" in text or "intern" in text:
        score += 15

    if "education" in text or "b.tech" in text or "degree" in text:
        score += 10

    keywords = ["developed", "built", "designed", "implemented", "created"]
    score += sum(2 for w in keywords if w in text)

    if len(text.split()) > 300:
        score += 10

    return min(score, 100)