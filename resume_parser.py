import os
import re
import docx2txt
import spacy
from pdfminer.high_level import extract_text

# Load pre-installed spaCy model
nlp = spacy.load("en_core_web_sm")

SKILLS_DB = [
    "Python", "Java", "C++", "SQL", "Machine Learning", "Deep Learning", "Data Analysis",
    "Excel", "Recruitment", "Sales", "Marketing", "Customer Service", "HR", "Communication",
    "AWS", "Linux", "Networking", "React", "Node.js", "Accounting", "Finance", "Teaching"
]

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".pdf":
        return extract_text(file_path)
    elif ext == ".docx":
        return docx2txt.process(file_path)
    return ""

def extract_name(nlp_text):
    for ent in nlp_text.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return ""

def extract_email(text):
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else ""

def extract_phone(text):
    match = re.search(r'(\+?\d{1,4}[\s-])?(?<!\d)(\d{10})(?!\d)', text)
    return match.group(2) if match else ""

def extract_skills(text):
    skills = []
    for skill in SKILLS_DB:
        if re.search(r'\b' + re.escape(skill) + r'\b', text, re.IGNORECASE):
            skills.append(skill)
    return ", ".join(skills)

def extract_companies(nlp_text):
    companies = [ent.text for ent in nlp_text.ents if ent.label_ == "ORG"]
    return ", ".join(set(companies[:3]))

def parse_resume(file_path):
    try:
        text = extract_text_from_file(file_path)
        nlp_text = nlp(text)

        return {
            "Name": extract_name(nlp_text),
            "Email": extract_email(text),
            "Phone": extract_phone(text),
            "Company": extract_companies(nlp_text),
            "Skills": extract_skills(text)
        }
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
        return {}
