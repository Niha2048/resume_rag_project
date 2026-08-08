import chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection("resumes")
model = SentenceTransformer("all-MiniLM-L6-v2")

def match_job(job_description, must_have_skills=None, min_experience=0):
    jd_vector = model.encode(job_description)
    results = collection.query(query_embeddings=[jd_vector], n_results=10, include=["documents","metadatas"])
    matches = []
    for rid, meta in zip(results["ids"][0], results["metadatas"][0]):
        skills = set(meta.get("Skills", []))
        exp = meta.get("ExperienceYears", 0)
        if must_have_skills and not set(must_have_skills).issubset(skills): continue
        if exp < min_experience: continue
        score = min(100, exp*8 + len(skills)*5)
        reasoning = f"Matched skills: {skills}, Experience: {exp} years"
        matches.append({
            "candidate_name": meta["Name"],
            "resume_path": meta["resume_path"],
            "match_score": score,
            "matched_skills": list(skills),
            "relevant_excerpts": [meta["Education"]],
            "reasoning": reasoning
        })
    return {"job_description": job_description, "top_matches": matches}

if __name__ == "__main__":
    jd = "Backend Developer with 5+ years Python experience, SQL, REST APIs, microservices"
    result = match_job(jd, must_have_skills=["python","sql"], min_experience=5)
    print(result)

















# import os
# import chromadb
# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity
# import json

# # ✅ Persistent client so it sees the same DB
# client = chromadb.PersistentClient(path="chroma_db")

# try:
#     client.delete_collection("resumes")
#     print("Old 'resumes' collection deleted.")
# except Exception:
#     print("No existing 'resumes' collection found.")

# collection = client.get_or_create_collection("resumes")

# # Embedding model
# model = SentenceTransformer("all-MiniLM-L6-v2")

# def load_job_description(file_path):
#     with open(file_path, "r", encoding="utf-8") as f:
#         return f.read()

# def keyword_match(text, keywords):
#     text_lower = text.lower()
#     return [kw for kw in keywords if kw.lower() in text_lower]

# def match_job(job_description, must_have=None, min_experience=None, top_k=10):
#     jd_vector = model.encode(job_description)
#     results = collection.query(
#         query_embeddings=[jd_vector],
#         n_results=top_k,
#         include=["documents", "metadatas", "embeddings"]
#     )

#     matches = []
#     critical_skills = must_have if must_have else []

#     for doc, meta, emb in zip(results["documents"][0], results["metadatas"][0], results["embeddings"][0]):
#         score = float(cosine_similarity([jd_vector], [emb])[0][0] * 100)
#         matched_skills = keyword_match(doc, critical_skills)

#         # Normalize experience years
#         years = meta.get("ExperienceYears", 0)
#         if isinstance(years, str):
#             try:
#                 years = int(years)
#             except:
#                 years = 0

#         # Must-have skills filter
#         if critical_skills and not matched_skills:
#             continue

#         # Must-have experience filter
#         if min_experience and years < min_experience:
#             continue

#         matches.append({
#             "candidate_name": meta.get("Name", os.path.basename(meta.get("resume_path", "Unknown")).replace(".txt", "")),
#             "resume_path": meta.get("resume_path", "Unknown"),
#             "match_score": round(score, 2),
#             "matched_skills": matched_skills,
#             "relevant_excerpts": [doc],
#             "reasoning": f"Matched on {meta.get('section','Unknown')} with skills {matched_skills} and {years} years experience"
#         })

#         # Debug print
#         print(meta.get("Name","Unknown"), years, matched_skills)

#     # Sort by score descending
#     matches = sorted(matches, key=lambda x: x["match_score"], reverse=True)

#     return matches if matches else None

# if __name__ == "__main__":
#     jd_text = load_job_description("job_descriptions/backend_dev.txt")
#     must_have_skills = ["Python", "SQL"]

#     print("\n--- Scenario 1: No filters ---")
#     baseline_matches = match_job(jd_text)
#     print({"job_description": jd_text, "top_matches": baseline_matches})

#     print("\n--- Scenario 2: Must-have skills only ---")
#     skill_matches = match_job(jd_text, must_have=must_have_skills)
#     print({"job_description": jd_text, "top_matches": skill_matches})

#     print("\n--- Scenario 3: Must-have skills + min experience ---")
#     exp_matches = match_job(jd_text, must_have=must_have_skills, min_experience=5)
#     print(json.dumps({"job_description": jd_text, "top_matches": exp_matches}, indent=2))
