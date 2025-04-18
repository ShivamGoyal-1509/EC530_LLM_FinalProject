import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_teaching_material(topic):
    prompt = f"Create a detailed teaching material for the topic: {topic}. Include key concepts, explanations, and examples."

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an expert educational content creator."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=700
    )

    return response.choices[0].message.content


def grade_assignment(text):
    prompt = f"""
    You are a strict but fair high school teacher. 
    Grade the following assignment. Provide:

    - A grade (A to F)
    - Numeric marks (0 to 100)
    - Constructive remarks

    Important: Format your response exactly like this:
    Grade: A
    Marks: 85
    Remarks: Your remarks here

    Assignment text:
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
    
    # More robust parsing logic
    grade = "N/A"
    marks = 0
    remarks = "No remarks provided."

    # Process each line looking for the specific prefixes
    for line in content.splitlines():
        line = line.strip()
        if line.lower().startswith("grade:"):
            grade = line.split(":", 1)[1].strip()
        elif line.lower().startswith("marks:"):
            try:
                # Extract only digits from the marks line
                marks = int(''.join(filter(str.isdigit, line.split(":", 1)[1].strip())))
            except ValueError:
                marks = 0
        elif line.lower().startswith("remarks:"):
            remarks = line.split(":", 1)[1].strip()
    
    return grade, marks, remarks