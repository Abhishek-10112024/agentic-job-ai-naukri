from typing import List
from app.schemas.job_schema import Job


def simple_score(job: Job) -> tuple:
    score = 0
    reason = []

    text = (job.title + " " + job.description).lower()

    # 🎯 Your profile alignment
    if "data science" in text:
        score += 25
        reason.append("Matches Data Science role")

    if "machine learning" in text or "ml" in text:
        score += 25
        reason.append("ML relevant")

    if "nlp" in text or "natural language processing" in text:
        score += 20
        reason.append("NLP match")

    if "deep learning" in text:
        score += 15
        reason.append("Deep Learning match")

    if "python" in text:
        score += 10
        reason.append("Python required")

    return score, ", ".join(reason)


def ranking_agent(state):
    jobs: List[Job] = state["jobs"]

    print("🧠 Ranking jobs...")

    ranked_jobs = []

    for job in jobs:
        score, reason = simple_score(job)

        job.score = score
        job.reason = reason

        ranked_jobs.append(job)

    # Sort descending
    ranked_jobs = sorted(ranked_jobs, key=lambda x: x.score, reverse=True)

    print("✅ Ranking complete")

    return {"jobs": ranked_jobs}