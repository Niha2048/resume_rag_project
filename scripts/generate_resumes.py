import os
import random

# Target folder
resume_dir = "../resumes"   # adjust path if needed
os.makedirs(resume_dir, exist_ok=True)

names = [
    "Gnanesh Elisetty", "Thejaswani ramigani", "Ashwini Rao", "Akhila chowdary", "Amrutha Boreddy",
    "Bhuvana Reddy", "Chandana Balaka", "Dhana sri", "Yamuna Naidu", "Phalguni Nair",
    "Gowthami chowdary", "Ramina Reddy", "Pavan kumar", "Naveen gindi", "Sai Gireesh",
    "Koteswar Rao", "Tharun sama", "Huzaifa shaik", "Rama Mohan", "Chintu sen",
    "Mani kanta", "Nirosha Erri", "Vydehi nambiar", "pradeep suchetty", "Pravallika VS",
    "Rohini Alipe", "Thanju pswamy", "Niveditha Erri", "Erri Teja Kumar", "Hemanth Naidu"
]

skills_pool = [
    ["Python", "SQL", "Machine Learning"],
    ["Java", "Spring Boot", "Microservices"],
    ["React", "JavaScript", "CSS"],
    ["AWS", "Docker", "Kubernetes"],
    ["C#", ".NET", "Azure"],
    ["Data Analysis", "R", "TensorFlow"],
    ["Project Management", "Agile", "Scrum"],
    ["Sitecore", "CMS", "Content Management"],
]

education_pool = [
    "B.Tech Computer Science",
    "B.Tech Computer Science - Artifiacial Intelligence",
    "B.Tech Electronics Communications",
    "M.Sc Software Engineering",
    "MBA",
    "PhD Artificial Intelligence",
    "B.Sc Information Technology",
    "M.Tech Data Science"
]

# Generate 30 resumes
for i, name in enumerate(names, 1):
    skills = random.choice(skills_pool)
    education = random.choice(education_pool)
    experience = random.randint(2, 12)

    resume_text = f"""Name: {name}
Skills: {', '.join(skills)}
Experience: {experience} years
Education: {education}
"""

    filename = os.path.join(resume_dir, f"{name.replace(' ', '_')}.txt")
    with open(filename, "w") as f:
        f.write(resume_text)

print("✅ 30 synthetic resumes generated in the 'resumes' folder.")
