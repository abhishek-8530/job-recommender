import pandas as pd
import os
import pdfplumber
import re
from rapidfuzz import fuzz

# =========================
# LOAD DATASET
# =========================
roles_path = os.path.join("data", "roles.csv")

if not os.path.exists(roles_path) or os.path.getsize(roles_path) == 0:
    raise ValueError("❌ roles.csv missing or empty!")

roles_df = pd.read_csv(roles_path)


# =========================
# CLEAN TEXT
# =========================
def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


# =========================
# EXTRACT TEXT FROM PDF
# =========================
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:   # FIX: avoid None
                text += page_text + " "
    return text


# =========================
# EXTRACT SKILLS (FIXED)
# =========================
def extract_skills(resume_text):
    resume_clean = clean_text(resume_text)
    found_skills = set()

    for skills in roles_df['skills']:
        skill_list = clean_text(skills).split()   # FIXED

        for skill in skill_list:
            # exact match
            if skill in resume_clean:
                found_skills.add(skill)
            else:
                # fuzzy match
                if fuzz.partial_ratio(skill, resume_clean) > 85:
                    found_skills.add(skill)

    return list(found_skills)


# =========================
# RECOMMEND JOBS (FIXED)
# =========================
def recommend_jobs(resume_text):
    resume_clean = clean_text(resume_text)
    extracted = extract_skills(resume_text)

    recommendations = []

    for _, row in roles_df.iterrows():
        role = row["role"]
        role_skills = clean_text(row["skills"]).split()

        match_count = 0

        for skill in role_skills:
            if skill in extracted:
                match_count += 1
            else:
                if fuzz.partial_ratio(skill, resume_clean) > 85:
                    match_count += 1

        match_percent = (match_count / len(role_skills)) * 100 if role_skills else 0

        recommendations.append({
            "role": role,
            "match_percent": round(match_percent, 2)
        })

    recommendations.sort(key=lambda x: x["match_percent"], reverse=True)
    return recommendations, extracted


# =========================
# MAIN TEST
# =========================
if __name__ == "__main__":
    resume_path = os.path.join("resumes", "sample_resume.pdf")

    if not os.path.exists(resume_path):
        print(f"❌ Resume file not found at: {resume_path}")
    else:
        print("📄 Extracting resume...")
        resume_text = extract_text_from_pdf(resume_path)

        if not resume_text.strip():
            print("❌ Failed to extract text from PDF")
        else:
            print("🔍 Matching skills...\n")

            recs, skills = recommend_jobs(resume_text)

            print("✅ Extracted Skills:")
            print(skills if skills else "No skills found")

            print("\n📊 Top Recommendations:")
            for r in recs[:10]:
                print(f"{r['role']} - {r['match_percent']}% match")