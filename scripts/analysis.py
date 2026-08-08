import time, chromadb
from sentence_transformers import SentenceTransformer

client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection("resumes")
model = SentenceTransformer("all-MiniLM-L6-v2")

job_descriptions = [
    ("Backend Developer", {"python","sql"}, 5),
    ("Data Scientist", {"python","machine learning"}, 3),
    ("Java Developer", {"java","spring boot","microservices"}, 4),
    ("Cloud Engineer", {"aws","docker","kubernetes"}, 3),
    ("Frontend Developer", {"react","javascript","css"}, 2)
]

for jd, skills, min_exp in job_descriptions:
    jd_vector = model.encode(jd)
    start = time.time()
    results = collection.query(query_embeddings=[jd_vector], n_results=10, include=["documents","metadatas"])
    end = time.time()
    retrieved = set(results["ids"][0])
    ground_truth = {
        rid for rid, meta in zip(results["ids"][0], results["metadatas"][0])
        if skills.issubset(set(meta.get("Skills",[]))) and meta.get("ExperienceYears",0) >= min_exp
    }
    tp = len(retrieved & ground_truth)
    fp = len(retrieved - ground_truth)
    fn = len(ground_truth - retrieved)
    precision = tp/(tp+fp) if (tp+fp)>0 else 0
    recall = tp/(tp+fn) if (tp+fn)>0 else 0
    print(f"\nJob: {jd}")
    print("Latency:", round(end-start,4),"s")
    print("Precision:", round(precision,2),"Recall:", round(recall,2))












# import time
# import chromadb
# from sentence_transformers import SentenceTransformer

# client = chromadb.PersistentClient(path="chroma_db")
# collection = client.get_or_create_collection("resumes")
# model = SentenceTransformer("all-MiniLM-L6-v2")

# jd = "Backend Developer with 5+ years Python experience, SQL, REST APIs, microservices"
# jd_vector = model.encode(jd)

# start = time.time()
# results = collection.query(
#     query_embeddings=[jd_vector],
#     n_results=10,
#     include=["documents","metadatas","embeddings"]
# )
# end = time.time()

# print("Latency:", round(end-start, 4), "seconds")
# print("Retrieved IDs:", results["ids"][0])

# # ✅ Build ground truth automatically
# expected_skills = {"Python","SQL"}
# ground_truth = {
#     rid for rid, meta in zip(results["ids"][0], results["metadatas"][0])
#     if expected_skills.issubset(set(meta.get("Skills",[]))) and meta.get("ExperienceYears",0) >= 5
# }

# retrieved = set(results["ids"][0])

# tp = len(retrieved & ground_truth)
# fp = len(retrieved - ground_truth)
# fn = len(ground_truth - retrieved)

# precision = tp / (tp+fp) if (tp+fp)>0 else 0
# recall = tp / (tp+fn) if (tp+fn)>0 else 0

# for rid, meta in zip(results["ids"][0], results["metadatas"][0]):
#     print(rid, "→", meta)
# print("Precision:", round(precision,2))
# print("Recall:", round(recall,2))
