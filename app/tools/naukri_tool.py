from playwright.sync_api import sync_playwright
from app.schemas.job_schema import Job
import os

STORAGE_PATH = "data/naukri_auth.json"


def fetch_naukri_jobs():
    jobs = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        # 🔐 SESSION HANDLING
        if os.path.exists(STORAGE_PATH):
            context = browser.new_context(storage_state=STORAGE_PATH)
            print("✅ Loaded saved session")
        else:
            context = browser.new_context()
            page = context.new_page()

            page.goto("https://www.naukri.com")

            print("👉 First-time login required")
            input("Login manually, then press ENTER...")

            # Save session
            context.storage_state(path=STORAGE_PATH)
            print("✅ Session saved for future use")

        page = context.new_page()

        # 🔥 DIRECTLY GO TO RECOMMENDED JOBS
        page.goto("https://www.naukri.com/mnjuser/recommendedjobs")

        # Wait for page + jobs to load
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_selector("article.jobTuple", timeout=15000)

        job_cards = page.query_selector_all("article.jobTuple")

        print(f"🧪 Found {len(job_cards)} job cards on page")

        for job in job_cards[:5]:
            try:
                # Title
                title_el = job.query_selector("p.title")
                title = title_el.inner_text().strip() if title_el else ""

                # Company
                company_el = job.query_selector(".companyInfo span[title]")
                company = company_el.inner_text().strip() if company_el else ""

                # Location
                location_el = job.query_selector(".location span")
                location = location_el.inner_text().strip() if location_el else ""

                # Description
                description_el = job.query_selector(".job-description span")
                description = (
                    description_el.get_attribute("title").strip()
                    if description_el and description_el.get_attribute("title")
                    else ""
                )

                # (Optional) Try extracting link
                link_el = job.query_selector("a")
                link = link_el.get_attribute("href") if link_el else ""

                jobs.append(
                    Job(
                        title=title,
                        company=company,
                        location=location,
                        description=description,
                        link=link if link else "",
                        source="Naukri"
                    )
                )

            except Exception as e:
                print("❌ Error parsing job:", e)
                continue

        browser.close()

    return jobs