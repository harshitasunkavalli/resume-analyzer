import pandas as pd
import re

def calculate_match_score(resume_skills, job_desc):

    if not job_desc or not resume_skills:
        return 0, []

    df = pd.read_csv("dataset/skills.csv")
    all_skills = df["skill"].dropna().str.lower().tolist()

    job_text = re.sub(r'[^a-z0-9\s]', ' ', job_desc.lower())

    jd_skills = []

    for skill in all_skills:
        skill = skill.strip()

        if len(skill) <= 2:
            continue

        if " " in skill:
            if skill in job_text:
                jd_skills.append(skill)
        else:
            if skill in job_text.split():
                jd_skills.append(skill)

    jd_skills = list(set(jd_skills))

    resume_clean = set([s.lower().strip() for s in resume_skills])

    matched = []
    for jd in jd_skills:
        for rs in resume_clean:
            if jd in rs or rs in jd:
                matched.append(jd)

    matched = list(set(matched))

    score = (len(matched) / len(jd_skills)) * 100 if jd_skills else 0
    missing_skills = [s for s in jd_skills if s not in matched]

    return round(score, 2), missing_skills[:10]