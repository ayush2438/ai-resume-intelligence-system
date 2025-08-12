import fitz  # PyMuPDF
import re
import json
import nltk
from nltk.corpus import stopwords
import string

# Download stopwords (only first time)
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# ---------------------------
# Step 1: Read PDF
# ---------------------------
def read_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# ---------------------------
# Step 2: Clean Text
# ---------------------------
def clean_text(text):
    """Removes noise from resume text."""
    # Remove extra spaces & newlines
    text = re.sub(r'\s+', ' ', text)
    # Remove weird symbols except common ones
    text = re.sub(r'[^\w\s@.,-]', '', text)
    return text.strip()

# ---------------------------
# Step 3: Split into Sections
# ---------------------------
def split_sections(text):
    """Splits resume into sections like education, experience, skills."""
    sections = {"education": "", "experience": "", "skills": ""}
    text_lower = text.lower()

    # Find keywords and split text
    edu_match = re.search(r'(education|academic background).*?(?=(experience|work experience|skills|$))', text_lower, re.DOTALL)
    exp_match = re.search(r'(experience|work experience).*?(?=(skills|education|$))', text_lower, re.DOTALL)
    skills_match = re.search(r'(skills).*?(?=(experience|education|$))', text_lower, re.DOTALL)

    if edu_match:
        sections["education"] = edu_match.group().strip()
    if exp_match:
        sections["experience"] = exp_match.group().strip()
    if skills_match:
        sections["skills"] = skills_match.group().strip()

    return sections

# ---------------------------
# Step 4: Basic Preprocessing
# ---------------------------
def preprocess_text(text):
    """Lowercase, remove punctuation & stopwords."""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    words = [w for w in words if w not in stop_words]
    return ' '.join(words)

# ---------------------------
# Step 5: Main
# ---------------------------
if __name__ == "__main__":
    resume_text = read_pdf("sample_resume.pdf")
    cleaned_text = clean_text(resume_text)
    sections = split_sections(cleaned_text)

    # Apply preprocessing to each section
    processed_sections = {k: preprocess_text(v) for k, v in sections.items()}

    # Save results
    data = {
        "raw_text": cleaned_text,
        "sections": processed_sections
    }

    with open("parsed_resume_day2.json", "w") as f:
        json.dump(data, f, indent=4)

    print("✅ Day 2 Parsing complete! Saved to parsed_resume_day2.json")
