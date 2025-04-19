import os
from openai import OpenAI  # OpenAI API client for AI model access
from dotenv import load_dotenv  # For loading environment variables from .env file

# Load environment variables from .env file
# This keeps API keys secure by not hardcoding them
load_dotenv()

# Initialize OpenAI client with API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to generate educational teaching material using AI
# Takes a topic string and returns generated content
def generate_teaching_material(topic):
    # Create a prompt asking the AI to generate educational content
    prompt = f"Create a detailed teaching material for the topic: {topic}. Include key concepts, explanations, and examples."

    # Make API call to OpenAI for content generation
    response = client.chat.completions.create(
        model="gpt-4o",  # Using GPT-4o model for higher quality content
        messages=[
            # Set system message to guide AI behavior
            {"role": "system", "content": "You are an expert educational content creator."},
            # Provide the user prompt with the topic
            {"role": "user", "content": prompt}
        ],
        max_tokens=700  # Limit response length to control output size
    )

    # Extract and return the generated content from the response
    return response.choices[0].message.content


# Function to grade an assignment or generated material using AI
# Takes text content and returns grade, marks, and remarks
def grade_assignment(text):
    # Create a detailed prompt instructing the AI how to grade
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

    # Make API call to OpenAI for grading evaluation
    response = client.chat.completions.create(
        model="gpt-4o",  # Using GPT-4o model for better evaluation
        messages=[
            # Set system message to establish AI role
            {"role": "system", "content": "You are an assignment evaluator."},
            # Provide the user prompt with the assignment text
            {"role": "user", "content": prompt}
        ],
        max_tokens=300  # Limit response length
    )

    # Extract response content
    content = response.choices[0].message.content
    
    # Initialize default values
    grade = "N/A"
    marks = 0
    remarks = "No remarks provided."

    # Parse the AI response to extract structured information
    # Process each line looking for specific prefixes
    for line in content.splitlines():
        line = line.strip()
        
        # Extract grade (A-F)
        if line.lower().startswith("grade:"):
            grade = line.split(":", 1)[1].strip()
            
        # Extract marks (0-100)
        elif line.lower().startswith("marks:"):
            try:
                # Extract only digits from the marks line
                # This handles cases where the AI includes non-numeric characters
                marks = int(''.join(filter(str.isdigit, line.split(":", 1)[1].strip())))
            except ValueError:
                # Default to 0 if conversion fails
                marks = 0
                
        # Extract remarks/feedback
        elif line.lower().startswith("remarks:"):
            remarks = line.split(":", 1)[1].strip()
    
    # Return the extracted grade, marks, and remarks as a tuple
    return grade, marks, remarks
