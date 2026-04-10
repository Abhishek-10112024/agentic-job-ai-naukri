import requests
from typing import List
from app.schemas.job_schema import Job
from app.config.profile import PROFILE


def call_ollama(prompt: str):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]


def llm_score(job: Job):
    prompt = f"""
You are an expert AI career advisor.

Candidate Profile:
{PROFILE}

Job:
Title: {job.title}
Company: {job.company}
Description: {job.description}

Evaluate VERY strictly.

Rules:
- You MUST differentiate jobs clearly
- DO NOT give same score unless identical
- Penalize:
  - Experience mismatch
  - Consulting roles
  - Lack of hands-on ML work
- Reward:
  - Strong ML/NLP/CV alignment
  - Hands-on engineering roles

Scoring:
- 90–100: Exceptional fit
- 75–89: Strong fit
- 60–74: Moderate fit
- 40–59: Weak fit
- 0–39: Poor fit

Also:
- Be critical, not generous
- Use full range of scores

Return ONLY JSON:
{{
  "score": number,
  "reason": "concise explanation"
}}
"""

    output = call_ollama(prompt)

    try:
        import json
        # Try extracting JSON safely
        start = output.find("{")
        end = output.rfind("}") + 1
        json_str = output[start:end]

        result = json.loads(json_str)

        return result.get("score", 0), result.get("reason", "No reason")
    except Exception as e:
        print("⚠️ Parsing error:", e)
        return 0, "Parsing failed"


def llm_ranking_agent(state):
    jobs: List[Job] = state["jobs"]

    print("🧠 LLM (Ollama) Ranking jobs...")

    for job in jobs:
        score, reason = llm_score(job)
        job.score = score
        job.reason = reason

    jobs = sorted(jobs, key=lambda x: x.score, reverse=True)

    print("✅ LLM Ranking complete")

    return {"jobs": jobs}