import fitz  # PyMuPDF
import re
import json

# ---------------------------
# Step 1: Read PDF File
# ---------------------------
def read_pdf(file_path):
    """Reads text from a PDF file."""
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# ---------------------------
# Step 2: Extract Email
# ---------------------------
def extract_email(text):
    """Finds the first email in the text."""
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    matches = re.findall(email_pattern, text)
    return matches[0] if matches else None

# ---------------------------
# Step 3: Extract Phone
# ---------------------------
def extract_phone(text):
    """Finds the first phone number in the text."""
    phone_pattern = r"\+?\d[\d\s-]{8,}\d"
    matches = re.findall(phone_pattern, text)
    return matches[0] if matches else None

# ---------------------------
# Step 4: Extract Name (Basic Logic)
# ---------------------------
def extract_name(text):
    """Finds a likely name (first line with <= 3 words)."""
    lines = text.split("\n")
    for line in lines:
        if line.strip() and len(line.split()) <= 3:  # Likely a name
            return line.strip()
    return None

# ---------------------------
# Step 5: Main Script
# ---------------------------
if __name__ == "__main__":
    resume_text = read_pdf("sample_resume.pdf")

    data = {
        "name": extract_name(resume_text),
        "email": extract_email(resume_text),
        "phone": extract_phone(resume_text)
    }

    # Save results in JSON
    with open("parsed_resume.json", "w") as f:
        json.dump(data, f, indent=4)

    print("✅ Resume parsed successfully! Data saved to parsed_resume.json")
    print(data)
