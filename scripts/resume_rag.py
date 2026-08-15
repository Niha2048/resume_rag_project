import os, re, chromadb
import json
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="chroma_db")

try:
    client.delete_collection("resumes")
    print("Old 'resumes' collection deleted.")
except Exception:
    print("No existing 'resumes' collection found.")

collection = client.get_or_create_collection("resumes")
model = SentenceTransformer("all-MiniLM-L6-v2")

def clean_skills(skills):
    return [s.strip().lower() for s in skills if s.strip()]

def extract_experience(text):
    match = re.search(r"(\d+)\s*(?:years|yrs)", text, re.IGNORECASE)
    return int(match.group(1)) if match else 0

def extract_skills(text):
    keywords = ["python","sql","machine learning","java","spring boot","microservices",
                "aws","docker","kubernetes","react","javascript","css","sitecore",
                "project management","agile","scrum"]
    found = [kw for kw in keywords if re.search(rf"\b{kw}\b", text, re.IGNORECASE)]
    return clean_skills(found) or ["unknown"]

def extract_education(text):
    match = re.search(r"(B\.Tech|M\.Tech|PhD|M\.Sc|B\.Sc)", text)
    return match.group(1) if match else "Unknown"

def process_resume(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    name = os.path.basename(file_path).replace(".txt", "")
    metadata = {
        "Name": name,
        "Skills": extract_skills(text),
        "ExperienceYears": extract_experience(text),
        "Education": extract_education(text),
        "resume_path": file_path,
        "section": "Full Resume"
    }
    embedding = model.encode(text)
    collection.add(documents=[text], metadatas=[metadata], ids=[name + "_1"])
    print(json.dumps(metadata, indent=2))

if __name__ == "__main__":
    for file in os.listdir("resumes"):
        if file.endswith(".txt"):
            process_resume(os.path.join("resumes", file))
    print("✅ Resumes processed and stored in ChromaDB with normalized metadata.")













# import os
# import re
# import chromadb
# from sentence_transformers import SentenceTransformer

# # ✅ Persistent client
# client = chromadb.PersistentClient(path="chroma_db")

# # 🔄 Automatic reset: delete and recreate collection
# try:
#     client.delete_collection("resumes")
#     print("Old 'resumes' collection deleted.")
# except Exception:
#     print("No existing 'resumes' collection found.")

# collection = client.get_or_create_collection("resumes")

# # Embedding model
# model = SentenceTransformer("all-MiniLM-L6-v2")

# # --- Helpers ---
# def clean_skills(skills):
#     """Normalize skills: strip spaces, lowercase."""
#     return [s.strip().lower() for s in skills if s.strip()]

# def extract_experience(text):
#     """Extract years of experience from resume text."""
#     match = re.search(r"(\d+)\s*(?:years|yrs)", text, re.IGNORECASE)
#     return int(match.group(1)) if match else 0

# def extract_skills(text):
#     """Extract skills from resume text (simple keyword match)."""
#     keywords = ["python","sql","machine learning","java","spring boot",
#                 "microservices","aws","docker","kubernetes","react",
#                 "javascript","css","project management","agile","scrum"]
#     found = []
#     for kw in keywords:
#         if re.search(rf"\b{kw}\b", text, re.IGNORECASE):
#             found.append(kw)
#     return clean_skills(found)

# def extract_education(text):
#     """Extract education info (simplified)."""
#     match = re.search(r"(B\.Tech|M\.Tech|PhD|M\.Sc|B\.Sc)", text)
#     return match.group(1) if match else "Unknown"

# # --- Resume Processing ---
# def process_resume(file_path):
#     with open(file_path, "r", encoding="utf-8") as f:
#         text = f.read()

#     name = os.path.basename(file_path).replace(".txt", "")
#     skills = extract_skills(text)
#     years = extract_experience(text)
#     education = extract_education(text)

#     metadata = {
#         "Name": name,
#         "Skills": skills,
#         "ExperienceYears": years,
#         "Education": education,
#         "resume_path": file_path,
#         "section": "Full Resume"
#     }

#     embedding = model.encode(text)

#     collection.add(
#         documents=[text],
#         metadatas=[metadata],
#         ids=[name + "_1"]
#     )

#     print("Stored:", metadata)

# # --- Main ---
# if __name__ == "__main__":
#     resumes_folder = "resumes"
#     for file in os.listdir(resumes_folder):
#         if file.endswith(".txt"):
#             process_resume(os.path.join(resumes_folder, file))

#     print("✅ Resumes processed and stored in ChromaDB with normalized metadata.")
