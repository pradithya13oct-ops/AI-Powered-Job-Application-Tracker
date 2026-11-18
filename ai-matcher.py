import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Common Technical Skills
SKILLS = [
    "python",
    "java",
    "javascript",
    "html",
    "css",
    "react",
    "django",
    "fastapi",
    "flask",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "pandas",
    "numpy",
    "scikit-learn",
    "streamlit",
    "git",
    "github",
    "docker",
    "aws",
    "linux",
    "rest api",
    "bootstrap",
    "communication",
    "problem solving"
]


# Extract Skills from Text
def extract_skills(text):

    text = text.lower()

    found_skills = []

    for skill in SKILLS:

        pattern = r'(?<!\w)' + re.escape(skill) + r'(?!\w)'

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills


# Calculate Resume and Job Description Match
def calculate_match(resume_text, job_description):

    resume_skills = extract_skills(resume_text)

    job_skills = extract_skills(job_description)

    if not job_skills:
        return {
            "match_percentage": 0,
            "matched_skills": [],
            "missing_skills": [],
            "resume_skills": resume_skills,
            "job_skills": []
        }

    matched_skills = list(
        set(resume_skills) & set(job_skills)
    )

    missing_skills = list(
        set(job_skills) - set(resume_skills)
    )

    # Skill Match Percentage
    skill_score = (
        len(matched_skills) / len(job_skills)
    ) * 100

    # Text Similarity
    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    try:

        vectors = vectorizer.fit_transform(documents)

        similarity = cosine_similarity(
            vectors[0:1],
            vectors[1:2]
        )[0][0] * 100

    except ValueError:

        similarity = 0

    # Final Match Score
    final_score = (
        skill_score * 0.70 +
        similarity * 0.30
    )

    return {
        "match_percentage": round(final_score, 2),
        "skill_match_percentage": round(skill_score, 2),
        "text_similarity": round(similarity, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "resume_skills": resume_skills,
        "job_skills": job_skills
    }


# Generate Career Recommendation
def get_recommendation(score):

    if score >= 80:
        return "Excellent Match! You can apply for this job."

    elif score >= 60:
        return "Good Match! Improve a few skills."

    elif score >= 40:
        return "Average Match. Learn the missing skills."

    else:
        return "Low Match. Improve your technical skills."


# Test the AI Matcher
if __name__ == "__main__":

    resume = """
    Python Developer with knowledge of Python,
    SQL, MySQL, HTML, CSS, JavaScript,
    Git, GitHub and FastAPI.
    """

    job_description = """
    We are looking for a Python Developer.

    Required Skills:
    Python, SQL, MySQL, Django,
    REST API, Git, AWS and Docker.
    """

    result = calculate_match(
        resume,
        job_description
    )

    print("\n===== AI JOB MATCHING REPORT =====")

    print(
        "Match Percentage:",
        result["match_percentage"], "%"
    )

    print(
        "Matched Skills:",
        result["matched_skills"]
    )

    print(
        "Missing Skills:",
        result["missing_skills"]
    )

    print(
        "Recommendation:",
        get_recommendation(
            result["match_percentage"]
        )
    )