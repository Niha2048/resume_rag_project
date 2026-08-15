from langgraph.graph import StateGraph, END
from dataclasses import dataclass, field
import json

# --- Agent State ---
@dataclass
class AgentState:
    history: list = field(default_factory=list)
    job_requirements: dict = field(default_factory=dict)
    candidate_shortlist: list = field(default_factory=list)
    reasoning: dict = field(default_factory=dict)

# --- Candidate Profiles (dummy data) ---
candidate_profiles = {
    "Ashwini_Rao": {"skills": ["Python", "SQL", "Machine Learning"], "experience": 7},
    "Chintu_sen": {"skills": ["Python", "SQL", "Machine Learning"], "experience": 10},
    "Erri_Teja_Kumar": {"skills": ["Java", "SQL", "Spring Boot"], "experience": 12},
    "Phalguni_Nair": {"skills": ["Python", "SQL", "Machine Learning"], "experience": 8},
}

# --- Core Nodes ---
def start_node(state: AgentState):
    state.history.append("Agent started")
    return state

def parse_jd_node(state: AgentState):
    jd = state.job_requirements.get("raw_jd", "")
    state.history.append(f"Parsed JD: {jd}")
    return state

def extract_requirements_node(state: AgentState):
    jd = state.job_requirements.get("raw_jd", "")
    must_have, nice_to_have = [], []
    if "React" in jd: must_have.append("React")
    if "Python" in jd: must_have.append("Python")
    if "SQL" in jd: must_have.append("SQL")
    if "Java" in jd: must_have.append("Java")
    if "Spring Boot" in jd: must_have.append("Spring Boot")
    if "microservices" in jd: nice_to_have.append("microservices")

    if "3+ years" in jd:
        state.job_requirements["min_experience"] = 3

    state.job_requirements["must_have"] = must_have
    state.job_requirements["nice_to_have"] = nice_to_have
    state.history.append(f"Extracted requirements: must={must_have}, nice={nice_to_have}")
    return state

def search_resumes_node(state: AgentState):
    must_have = state.job_requirements.get("must_have", [])
    min_exp = state.job_requirements.get("min_experience", 0)

    shortlist = []
    for c, profile in candidate_profiles.items():
        if all(req in profile["skills"] for req in must_have) and profile["experience"] >= min_exp:
            shortlist.append(c)

    state.candidate_shortlist = shortlist
    state.history.append(f"Shortlisted candidates: {shortlist}")
    return state

def rank_candidates_node(state: AgentState):
    scores = {}
    for c in state.candidate_shortlist:
        profile = candidate_profiles[c]
        scores[c] = f"{profile['experience']} years exp, skills={profile['skills']}"
    state.reasoning = scores
    state.history.append("Ranked candidates")
    return state

def generate_report_node(state: AgentState):
    report = {
        "job_description": state.job_requirements.get("raw_jd", ""),
        "top_matches": state.candidate_shortlist,
        "reasoning": state.reasoning
    }
    print(json.dumps(report, indent=2))
    state.history.append("Generated report")
    return state

# --- Advanced Features ---
def refine_requirements_node(state: AgentState, new_req: str):
    must_have = state.job_requirements.get("must_have", [])
    must_have.append(new_req)
    state.job_requirements["must_have"] = must_have
    state.history.append(f"Refined requirements: added {new_req}")
    state = search_resumes_node(state)
    state = rank_candidates_node(state)
    return state

def explain_ranking_node(state: AgentState, c1: str, c2: str):
    r1 = state.reasoning.get(c1, "No reasoning available")
    r2 = state.reasoning.get(c2, "No reasoning available")
    explanation = f"{c1}: {r1}\n{c2}: {r2}"
    print("Ranking explanation:\n", explanation)
    state.history.append(f"Explained ranking between {c1} and {c2}")
    return state

def multi_round_screening_node(state: AgentState):
    round1 = state.candidate_shortlist[:10]
    round2 = [c for c in round1 if "Python" in candidate_profiles[c]["skills"]]
    recommendations = {
        c: "Hire" if candidate_profiles[c]["experience"] >= 10 else "No-hire"
        for c in round2
    }
    print("Multi-round screening results:", json.dumps(recommendations, indent=2))
    state.history.append("Completed multi-round screening")
    return state

def compare_candidates_node(state: AgentState, candidates: list):
    comparison = {}
    for c in candidates:
        comparison[c] = state.reasoning.get(c, "No reasoning available")
    print("Candidate comparison:\n", json.dumps(comparison, indent=2))
    state.history.append(f"Compared candidates: {candidates}")
    return state

def strengths_gaps_node(state: AgentState):
    analysis = {}
    for c, profile in candidate_profiles.items():
        strengths, gaps = [], []
        if "Java" in profile["skills"]:
            strengths.append("Strong in Java")
        else:
            gaps.append("Missing Java")
        if "AWS" in profile["skills"]:
            strengths.append("Cloud experience")
        else:
            gaps.append("Needs cloud experience")
        if profile["experience"] >= 10:
            strengths.append("Senior-level experience")
        else:
            gaps.append("Limited experience compared to peers")
        analysis[c] = {"strengths": strengths, "gaps": gaps}
    print("Strengths & Gaps:\n", json.dumps(analysis, indent=2))
    state.history.append("Generated strengths & gaps analysis")
    return state

def improvement_suggestions_node(state: AgentState):
    suggestions = {}
    for c, profile in candidate_profiles.items():
        advice = []
        if profile["experience"] < 10:
            advice.append("Gain more senior-level project experience")
        if "AWS" not in profile["skills"]:
            advice.append("Upskill in cloud technologies (AWS/Azure)")
        if advice:
            suggestions[c] = " | ".join(advice)
    print("Improvement suggestions:\n", json.dumps(suggestions, indent=2))
    state.history.append("Generated improvement suggestions")
    return state

# --- Graph Workflow ---
graph = StateGraph(AgentState)
graph.add_node("START", start_node)
graph.add_node("ParseJD", parse_jd_node)
graph.add_node("ExtractReqs", extract_requirements_node)
graph.add_node("SearchResumes", search_resumes_node)
graph.add_node("RankCandidates", rank_candidates_node)
graph.add_node("GenerateReport", generate_report_node)

graph.add_edge("START","ParseJD")
graph.add_edge("ParseJD","ExtractReqs")
graph.add_edge("ExtractReqs","SearchResumes")
graph.add_edge("SearchResumes","RankCandidates")
graph.add_edge("RankCandidates","GenerateReport")
graph.add_edge("GenerateReport", END)

graph.set_entry_point("START")
workflow = graph.compile()

# --- CLI Interface ---
if __name__ == "__main__":
    state = AgentState()
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        if user_input.lower().startswith("add "):
            new_req = user_input[4:].strip()
            state = refine_requirements_node(state, new_req)

        elif user_input.lower().startswith("why did"):
            parts = user_input.split()
            if len(parts) >= 6:
                c1, c2 = parts[2], parts[-1]
                state = explain_ranking_node(state, c1, c2)

        elif "screening" in user_input.lower():
            state = multi_round_screening_node(state)

        elif user_input.lower().startswith("compare"):
            parts = user_input.split()
            candidates = [p for p in parts[1:] if p in candidate_profiles]
            state = compare_candidates_node(state, candidates)

        elif "strengths" in user_input.lower() or "gaps" in user_input.lower():
            state = strengths_gaps_node(state)

        elif "improvement" in user_input.lower():
            state = improvement_suggestions_node(state)

        else:
            state.job_requirements["raw_jd"] = user_input
            result = workflow.invoke(state)
            if isinstance(result, dict):
                state = AgentState(
                    history=result.get("history", []),
                    job_requirements=result.get("job_requirements", {}),
                    candidate_shortlist=result.get("candidate_shortlist", []),
                    reasoning=result.get("reasoning", {})
                )
            elif isinstance(result, AgentState):
                state = result

        print("Agent history:", state.history)
