import fitz  # PyMuPDF
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def grade_assignment(text):
    prompt = f"""
You are a strict but fair high school teacher evaluating a student's assignment.

Please analyze the text below and provide:
1. Grade (A to F)
2. Marks (0 to 100)
3. Constructive, personalized feedback (2-3 sentences)

Respond only in this format (each on a new line):
Grade: A
Marks: 85
Remarks: Very well-structured and insightful work. Great effort!

---
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an assignment evaluator."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )

    content = response.choices[0].message.content

    # TEMP: Print the raw response for debug
    print("\n--- GPT Response Start ---\n", content, "\n--- GPT Response End ---\n")

    grade = "N/A"
    marks = 0
    remarks = "No remarks provided."

    # Robust extraction using lowercased line prefixes
    for line in content.splitlines():
        line = line.strip()
        if line.lower().startswith("grade:"):
            grade = line.split(":", 1)[1].strip()
        elif line.lower().startswith("marks:"):
            try:
                marks = int(''.join(filter(str.isdigit, line.split(":", 1)[1].strip())))
            except ValueError:
                marks = 0
        elif line.lower().startswith("remarks:"):
            remarks = line.split(":", 1)[1].strip()

    return grade, marks, remarks