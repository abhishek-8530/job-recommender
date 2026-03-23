import streamlit as st
import os
import pandas as pd
import pdfplumber
import re
from rapidfuzz import fuzz

# =========================
# LOAD DATA
# =========================
roles_path = os.path.join("data", "roles.csv")

if not os.path.exists(roles_path) or os.path.getsize(roles_path) == 0:
    st.error("❌ roles.csv file is missing or empty!")
    st.stop()

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
def extract_text_from_pdf(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
    return text


# =========================
# EXTRACT SKILLS (FIXED)
# =========================
def extract_skills(resume_text):
    resume_clean = clean_text(resume_text)
    found_skills = set()

    for skills in roles_df['skills']:
        # FIX: split by space instead of ;
        skill_list = clean_text(skills).split()

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
            "Role": role,
            "Match %": round(match_percent, 2)
        })

    recommendations.sort(key=lambda x: x["Match %"], reverse=True)
    return recommendations, extracted


# =========================
# STREAMLIT UI
# =========================
st.set_page_config(page_title="Job Recommender", page_icon="💼")

st.title("💼 Job Recommender System")
st.write("Upload your resume PDF to get job recommendations.")

uploaded_file = st.file_uploader("📂 Upload Resume (PDF only)", type=["pdf"])

if uploaded_file is not None:
    st.success("✅ Resume uploaded successfully!")

    resume_text = extract_text_from_pdf(uploaded_file)

    if not resume_text.strip():
        st.error("❌ Could not extract text from PDF!")
        st.stop()

    recs, skills = recommend_jobs(resume_text)

    st.subheader("📌 Extracted Skills:")
    st.write(", ".join(skills) if skills else "No skills found.")

    st.subheader("📊 Job Recommendations:")
    st.dataframe(recs[:100])  # show top 100