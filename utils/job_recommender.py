import pandas as pd

def recommend_jobs(skills):

    df = pd.read_csv("dataset/job_roles.csv")

    results = []

    skills = [s.lower().strip() for s in skills]

    for _, row in df.iterrows():

        role = str(row["job_role"]).strip()
        req = str(row["skills"]).lower().replace(" ", "").split(",")

        match = sum(1 for s in skills if s in req)

        if match > 0:
            score = (match / len(req)) * 100
            results.append((role, score))

    results.sort(key=lambda x: x[1], reverse=True)

    jobs = [r[0] for r in results[:5]]

    best_job = jobs[0] if jobs else "No match found"

    return best_job, jobs