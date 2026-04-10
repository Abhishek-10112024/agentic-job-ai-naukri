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


def generate_resume_content(job: Job):
    prompt = f"""
You are an expert resume writer.

Candidate Profile:
{PROFILE}

Job:
Title: {job.title}
Company: {job.company}
Description: {job.description}

Generate:

1. 3 strong resume bullet points tailored for this job
2. A short personalized cover message (3–4 lines)

Guidelines:
- Use specific skills (NLP, LSTM, CNN, Python)
- Make it ATS-friendly
- Keep it concise and impactful

Return in this format:

RESUME_BULLETS:
- ...
- ...
- ...

COVER_MESSAGE:
...
"""

    return call_ollama(prompt)


def resume_agent(state):
    jobs: List[Job] = state["jobs"]

    print("📄 Generating resume content for top jobs...")

    top_jobs = jobs[:3]

    for job in top_jobs:
        output = generate_resume_content(job)

        print(f"\n🎯 {job.title} at {job.company}")
        print(output)
        print("=" * 60)

    return state