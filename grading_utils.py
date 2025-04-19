import fitz  # PyMuPDF library for PDF processing
import os
from openai import OpenAI  # OpenAI API client
from dotenv import load_dotenv  # For loading environment variables

# Load environment variables from .env file
# This helps keep API keys and secrets out of source code
load_dotenv()

# Initialize OpenAI client with API key - with error handling
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    client = OpenAI(api_key=api_key)
else:
    # For testing purposes, create a mock
    import unittest.mock
    client = unittest.mock.MagicMock()
    print("Warning: No OpenAI API key found. Using mock client.")

# Function to extract all text content from a PDF file
# Takes a file path and returns the full text as a string
def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF document
    
    Args:
        file_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text content from all pages
    """
    # Open the PDF document
    doc = fitz.open(file_path)
    
    # Initialize empty string to store text
    text = ""
    
    # Loop through each page and extract text
    for page in doc:
        text += page.get_text()
        
    # Return the combined text from all pages
    return text

# Function to grade an assignment using OpenAI's GPT model
# Takes assignment text and returns grade, marks, and feedback
def grade_assignment(text):
    """
    Grade an assignment using AI
    
    Args:
        text (str): The assignment text to grade
        
    Returns:
        tuple: (grade, marks, remarks) containing the assessment
    """
    # Construct a detailed prompt for the AI to evaluate the assignment
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

    # Make API call to OpenAI for assignment evaluation
    response = client.chat.completions.create(
        model="gpt-4o",  # Using GPT-4o model for better evaluation
        messages=[
            {"role": "system", "content": "You are an assignment evaluator."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300  # Limit response length
    )

    # Extract response content
    content = response.choices[0].message.content

    # Debug: Print raw AI response
    print("\n--- GPT Response Start ---\n", content, "\n--- GPT Response End ---\n")

    # Initialize default values
    grade = "N/A"
    marks = 0
    remarks = "No remarks provided."

    # Parse the AI response to extract grade, marks, and remarks
    # This uses a robust approach checking each line for specific prefixes
    for line in content.splitlines():
        line = line.strip()
        
        # Extract grade (A-F)
        if line.lower().startswith("grade:"):
            grade = line.split(":", 1)[1].strip()
            
        # Extract marks (0-100)
        elif line.lower().startswith("marks:"):
            try:
                # Extract only numeric digits from the marks line
                marks = int(''.join(filter(str.isdigit, line.split(":", 1)[1].strip())))
            except ValueError:
                # Default to 0 if conversion fails
                marks = 0
                
        # Extract remarks/feedback
        elif line.lower().startswith("remarks:"):
            remarks = line.split(":", 1)[1].strip()

    # Return the extracted grade, marks, and remarks as a tuple
    return grade, marks, remarks
