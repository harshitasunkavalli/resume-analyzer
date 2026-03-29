import pandas as pd
import re

# 🔹 Load skills dataset
skills_df = pd.read_csv("dataset/skills.csv")
skills_list = skills_df["skill"].dropna().str.lower().str.strip().tolist()

def extract_skills(text):

    if not text:
        return []

    text = text.lower()

    # 🔥 clean text
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    words = set(text.split())

    detected = set()

    for skill in skills_list:

        skill = skill.strip()

        # ❌ skip very small skills (important fix)
        if len(skill) <= 2:
            continue

        # ✅ multi-word skill
        if " " in skill:
            if skill in text:
                detected.add(skill)

        # ✅ single-word exact match
        else:
            if skill in words:
                detected.add(skill)

    return list(detected)