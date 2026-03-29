from flask import Flask, render_template, request, send_file
import os, uuid

from utils.ats_score import calculate_ats_score
from utils.skill_extractor import extract_skills
from utils.matcher import calculate_match_score
from utils.job_recommender import recommend_jobs
from utils.feedback import generate_feedback
from utils.pdf_generator import generate_pdf
from utils.resume_parser import extract_text_from_pdf

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
PDF_FOLDER = "reports"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PDF_FOLDER, exist_ok=True)


# 🔥 GENERIC LEARNING RECOMMENDATION
def recommend_learning(skills):

    skills = [s.lower() for s in skills]
    rec = []

    categories = {
        "frontend": ["html", "css", "javascript"],
        "backend": ["python", "java", "node", "django", "flask"],
        "database": ["sql", "mongodb", "mysql"],
        "tools": ["git", "github"],
        "data": ["pandas", "numpy", "machine learning"]
    }

    trending = {
        "frontend": ["react"],
        "backend": ["node", "django"],
        "database": ["mongodb"],
        "tools": ["git"],
        "data": ["machine learning"]
    }

    for category, base in categories.items():
        if any(s in skills for s in base):
            for t in trending[category]:
                if t not in skills:
                    rec.append(f"Learn {t.capitalize()} for {category} development")

    if "git" not in skills:
        rec.append("Learn Git & GitHub for version control")

    if len(skills) < 5:
        rec.append("Improve your profile by adding more technical skills")

    return list(set(rec))[:5]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files.get("resume")
    job_desc = request.form.get("job_desc", "")

    if not file:
        return "No file uploaded"

    filename = str(uuid.uuid4()) + ".pdf"
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)

    # 🔥 PROCESS
    text = extract_text_from_pdf(file_path)
    skills = extract_skills(text)

    ats_score = calculate_ats_score(skills, text)
    match_score, missing_skills = calculate_match_score(skills, job_desc)

    best_job, jobs = recommend_jobs(skills)
    feedback = list(generate_feedback(skills, missing_skills, ats_score))

    # 🔥 NEW FEATURE
    learning = recommend_learning(skills)

    # PDF
    pdf_filename = str(uuid.uuid4()) + ".pdf"
    pdf_path = os.path.join(PDF_FOLDER, pdf_filename)

    generate_pdf(pdf_path, ats_score, match_score, skills, jobs, feedback)

    return render_template(
        "result.html",
        score=ats_score,
        match_score=match_score,
        skills=skills,
        jobs=jobs,
        best_job=best_job,
        feedback=feedback,
        pdf_file=pdf_filename,
        learning=learning
    )


@app.route("/download/<filename>")
def download(filename):
    return send_file(os.path.join(PDF_FOLDER, filename), as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)