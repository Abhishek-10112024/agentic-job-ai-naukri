from app.tools.naukri_tool import fetch_naukri_jobs

def job_finder_agent(state):
    print("🔍 Fetching jobs from Naukri...")

    jobs = fetch_naukri_jobs()

    print(f"✅ Found {len(jobs)} jobs")

    return {"jobs": jobs}