# 🤖 Smart Resume Screener

AI-powered resume screening and job matching system built with Python, Streamlit, Gemini AI, PyMuPDF, and SQLite.

## 📌 Overview

Smart Resume Screener helps recruiters analyze multiple resumes against a given job description and automatically rank candidates based on their suitability.

The application uses Gemini AI to extract relevant information from resumes, compare candidate skills with job requirements, calculate a match score, and provide an AI-generated justification for the score.

## ✨ Features

* 📄 Upload multiple PDF resumes
* 📝 Enter a job description
* 🤖 AI-powered resume analysis using Gemini
* 🎯 Candidate match score from 0–100
* ✅ Automatic candidate shortlisting
* 🧠 AI-generated justification for each match score
* 🔍 Matching and missing skills identification
* 🎓 Education extraction
* 💼 Experience extraction
* 💪 Candidate strengths
* 📈 Improvement recommendations
* 📊 Candidate ranking
* ⚖️ Candidate comparison
* 🔎 Recruiter search and score filters
* 🏆 Shortlisted-candidate filtering
* 📥 Export candidate results as CSV
* 💾 SQLite database for storing candidate results
* 🔄 Automatic retry handling for temporary Gemini API errors

## 🛠️ Tech Stack

| Technology    | Purpose                                |
| ------------- | -------------------------------------- |
| Python        | Core application logic                 |
| Streamlit     | Web application interface              |
| Gemini AI     | Resume analysis and candidate matching |
| PyMuPDF       | PDF text extraction                    |
| SQLite        | Candidate data storage                 |
| Pandas        | Data processing and CSV export         |
| python-dotenv | Environment variable management        |

## 🏗️ Project Structure

```text
smart-resume-screener/
│
├── app.py                 # Streamlit application
├── database.py            # SQLite database operations
├── llm_service.py         # Gemini AI integration
├── requirements.txt       # Python dependencies
├── .gitignore             # Files excluded from Git
└── README.md              # Project documentation
```

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/SuhanaJena/smart-resume-screener.git
cd smart-resume-screener
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

**macOS/Linux:**

```bash
source venv/bin/activate
```

**Windows:**

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 🔑 Gemini API Configuration

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_api_key_here
```

Replace `your_api_key_here` with your Gemini API key.

⚠️ **Never commit your `.env` file or API key to GitHub.**

## ▶️ Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open locally in your browser.

## 🔄 Application Workflow

```text
Upload Resumes
       ↓
Extract PDF Text
       ↓
Enter Job Description
       ↓
Gemini AI Analysis
       ↓
Extract Candidate Information
       ↓
Calculate Match Score
       ↓
Generate AI Justification
       ↓
Store Results in SQLite
       ↓
Rank & Shortlist Candidates
       ↓
Compare Candidates
       ↓
Export Results
```

## 📊 Example

For a Junior Software Engineer position, the system can identify:

**Matching skills**

* Python
* Java
* Web Technologies
* Data Structures and Algorithms

**Missing skills**

* SQL
* Git
* Databases

The system then generates a match score and explains the reasoning behind the score.

## 🧠 AI Analysis

Gemini AI analyzes the relationship between the job description and each candidate's resume.

For every candidate, the system generates:

* Candidate name
* Match score
* Candidate summary
* Matching skills
* Missing skills
* Education
* Experience
* Strengths
* Recommendations
* AI justification

Temporary Gemini API failures such as `503 UNAVAILABLE` and `429 RESOURCE_EXHAUSTED` are handled using automatic retries.

## 💾 Database

Candidate results are stored using SQLite.

The application prevents duplicate records for the same resume filename by updating an existing candidate instead of creating another record.

The SQLite database is generated locally when the application runs.

## 🔐 Security

Sensitive configuration files should not be committed to the repository.

The following files should be excluded through `.gitignore`:

```text
.env
resume_screener.db
__pycache__/
*.pyc
venv/
.venv/
```

## 🚀 Future Improvements

* 🌐 Public cloud deployment
* 📧 Recruiter email notifications
* 👤 User authentication
* 📑 Support for DOCX resumes
* 📊 Advanced recruiter analytics
* 🧠 More detailed candidate-job matching
* 📈 Visual analytics dashboard
* ☁️ Cloud database integration

## 👩‍💻 Author

**Suhana Jena**

GitHub: https://github.com/SuhanaJena
