# 📄 Resume RAG Project

## 🔹 Overview
This project implements a **Retrieval-Augmented Generation (RAG) system** for **resume–job description matching**. It leverages document chunking, embeddings, and vector databases to enable **semantic search** and hybrid filtering.

---

## 🔹 Learning Objectives
- **Document chunking** and embedding  
- **Vector database** construction  
- **Retrieval pipelines** for resumes  
- **Semantic search** for job matching  

---

## 🔹 Architecture
1. **resume_rag.py**  
   - Loads resumes from filesystem  
   - Chunks intelligently (Education, Experience, Skills)  
   - Generates embeddings via HuggingFace `sentence-transformers`  
   - Stores in **ChromaDB** with normalized metadata (Name, Skills, ExperienceYears, Education)  

2. **job_matcher.py**  
   - Accepts job description input  
   - Converts JD to embedding  
   - Retrieves top‑K resumes (K=10)  
   - Implements **hybrid search** (semantic + keyword)  
   - Scores matches (0–100) and provides reasoning  

3. **analysis.py**  
   - Runs experimentation across 5 job descriptions  
   - Measures **latency** and **retrieval accuracy (precision/recall)**  
   - Prints summary metrics  

---

## 🔹 Output Format
```json
{
  "job_description": "...",
  "top_matches": [
    {
      "candidate_name": "Hemanth Kumar",
      "resume_path": "resumes/hemanth_kumar.txt",
      "match_score": 92,
      "matched_skills": ["Python", "Machine Learning"],
      "relevant_excerpts": ["..."],
      "reasoning": "Strong match for ML experience..."
    }
  ]
}
```

---

## 🔹 Folder Structure
```
resume_rag_project/
│
├── resumes/                # 30+ diverse resume text files
├── job_descriptions/        # 5+ job description text files
├── scripts/
│   ├── resume_rag.py        # ingestion pipeline
│   ├── job_matcher.py       # matching engine
│   ├── analysis.py          # metrics & experimentation
├── chroma_db/               # vector database storage
└── README.md                # project documentation
```

---

## 🔹 Usage
1. **Ingest resumes**  
   ```bash
   python scripts/resume_rag.py
   ```

2. **Run job matcher**  
   ```bash
   python scripts/job_matcher.py
   ```

3. **Run analysis (metrics)**  
   ```bash
   python scripts/analysis.py
   ```

---

## 🔹 Deliverables
- ✅ Complete RAG implementation  
- ✅ Dataset: 30+ resumes, 5+ job descriptions  
- ✅ Scripts: ingestion, matching, analysis  
- ✅ Performance metrics: latency, precision, recall  
- ✅ Demo video: 3–4 minutes showing ingestion, matching, and analysis  

---

## 🔹 Future Enhancements
- Add support for **REST API endpoints** for job matching  
- Integrate **Pinecone/Weaviate** for scalable vector storage  
- Expand **skill extraction** with NLP models for richer metadata  
- Build a **web UI** for interactive job–resume matching  

