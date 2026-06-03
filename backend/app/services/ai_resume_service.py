import spacy
from difflib import get_close_matches

nlp = spacy.load("en_core_web_sm")

# =========================
# SKILL DATABASE
# =========================

SKILL_ALIASES = {
    "Python": ["python", "paython"],
    "React": ["react", "reactjs", "react.js"],
    "JavaScript": ["javascript", "js"],
    "MongoDB": ["mongodb", "mangodb", "mongo db"],
    "FastAPI": ["fastapi", "fast api"],
    "Tailwind": ["tailwind", "tailwindcss"],
    "Node.js": ["node", "nodejs", "node.js"],
    "Machine Learning": [
        "machine learning",
        "machine learing",
        "ml"
    ],
    "AI": [
        "ai",
        "artificial intelligence"
    ],
    "SQL": ["sql", "mysql", "postgresql"],
    "HTML": ["html"],
    "CSS": ["css"],
    "Django": ["django"],
    "Flask": ["flask"],
    "C++": ["c++", "cpp"],
    "Java": ["java"]
}

# =========================
# EXTRACT SKILLS
# =========================

def extract_skills(resume_text):

    found_skills = []

    text = resume_text.lower()

    doc = nlp(text)

    processed_text = " ".join([token.text for token in doc])

    for main_skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            # DIRECT MATCH
            if alias.lower() in processed_text:

                if main_skill not in found_skills:

                    found_skills.append(main_skill)

            # FUZZY MATCH
            else:

                words = processed_text.split()

                close_match = get_close_matches(
                    alias.lower(),
                    words,
                    n=1,
                    cutoff=0.85
                )

                if close_match:

                    if main_skill not in found_skills:

                        found_skills.append(main_skill)

    return found_skills


# =========================
# MATCH SCORE
# =========================

def calculate_match_score(resume_skills, job_skills):

    matched_skills = []

    missing_skills = []

    # LOWERCASE NORMALIZATION
    normalized_resume_skills = [
        skill.lower()
        for skill in resume_skills
    ]

    for skill in job_skills:

        if skill.lower() in normalized_resume_skills:

            matched_skills.append(skill)

        else:

            missing_skills.append(skill)

    # SCORE CALCULATION
    if len(job_skills) == 0:

        score = 0

    else:

        score = int(
            (len(matched_skills) / len(job_skills)) * 100
        )

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "score": score
    }