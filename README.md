# job-recommender
💼 Job Recommender System is a Streamlit-based web app that analyzes resumes (PDF) and matches skills with job roles using NLP and fuzzy matching. It extracts skills, calculates match scores, and recommends the most relevant roles, improving accuracy over basic keyword systems.

🚀 Features
📄 Upload resume in PDF format
🧠 Extracts text using pdfplumber
🧹 Cleans and preprocesses text
🔍 Extracts skills using keyword + fuzzy matching
📊 Matches resume with job roles dataset
💼 Recommends top job roles with match percentage
⚡ Fast and interactive UI using Streamlit


🛠️ Tech Stack
Python
Streamlit
Pandas
pdfplumber
RapidFuzz (for fuzzy matching)
Regex (text cleaning)


📂 Project Structure
project/
│── data/
│   └── roles.csv          # Dataset (roles + skills)
│
│── resumes/
│   └── sample_resume.pdf  # Test resume
│
│── app.py                 # Streamlit UI
│── parser.py              # Resume parsing & recommendation logic
│── load_dataset.py        # Dataset loader
│
│── requirements.txt
│── README.md


▶️ Run the App
streamlit run app.py


🧠 How It Works
Extract text from uploaded PDF
Clean and normalize text
Compare resume skills with dataset
Use fuzzy matching (RapidFuzz) for better accuracy
Calculate match percentage
Display top job recommendations


📌 Example Output
Extracted Skills: python, sql, machine learning
Recommendations:
Data Scientist – 85%
Data Analyst – 78%
ML Engineer – 72%


📜 License

This project is open-source and available under the MIT License.

👨‍💻 Author

Your Name
GitHub: https://github.com/abhishek-8530


