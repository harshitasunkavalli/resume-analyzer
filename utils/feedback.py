def generate_feedback(skills, missing_skills, ats_score):

    feedback = []

    if ats_score >= 80:
        feedback.append("Your resume is strong for ATS systems.")
    else:
        feedback.append("Improve your resume ATS score by adding more relevant skills.")

    if missing_skills:
        feedback.append("Add missing skills: " + ", ".join(missing_skills))

    feedback.append("Use action words like Developed, Built, Designed.")
    feedback.append("Add measurable achievements (e.g., improved performance by 30%).")

    return feedback