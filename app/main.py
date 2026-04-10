from app.graph.job_graph import graph
import json
import os

if __name__ == "__main__":
    result = graph.invoke({"jobs": []})

    print("\n🎯 FINAL RANKED JOBS:\n")

    for job in result["jobs"]:
        print(f"🔹 {job.title} at {job.company}")
        print(f"   Score: {job.score}")
        print(f"   Reason: {job.reason}")
        print("-" * 50)

    # ✅ CREATE data folder if not exists
    os.makedirs("data", exist_ok=True)

    # ✅ SAVE OUTPUT FOR UI
    with open("data/sample_output.json", "w") as f:
        json.dump(
            {
                "jobs": [job.__dict__ for job in result["jobs"]]
            },
            f,
            indent=2
        )

    print("\n✅ Sample output saved to data/sample_output.json")