from langgraph.graph import StateGraph
from typing import TypedDict, List
from app.schemas.job_schema import Job
from app.agents.job_finder import job_finder_agent
# from app.agents.ranking_agent import ranking_agent
from app.agents.llm_ranking_agent import llm_ranking_agent
from app.agents.resume_agent import resume_agent

class JobState(TypedDict):
    jobs: List[Job]

builder = StateGraph(JobState)

builder.add_node("job_finder", job_finder_agent)
# builder.add_node("ranking", ranking_agent)
builder.add_node("ranking", llm_ranking_agent)
builder.add_node("resume", resume_agent)

builder.set_entry_point("job_finder")

builder.add_edge("job_finder", "ranking")

builder.add_edge("ranking", "resume")

graph = builder.compile()