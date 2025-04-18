# Document Analyzer for Teachers

This Streamlit web application allows teachers to upload student assignments or generate teaching material using AI, automatically grade assignments, provide feedback, and store results in a local database. An admin panel is also included to manage the database.

## Features

### Teacher Mode
- Upload a student's assignment in PDF format.
- Generate teaching material using OpenAI GPT-4o.
- Automatically grade assignments and provide constructive feedback.
- Save teacher name, email, student name, grade, marks, and remarks into a SQLite database.
- View all past submissions via a button in the sidebar.

### Admin Mode
- Secure admin login with predefined credentials:
  - Username: `admin`
  - Password: `qwerty`
- Delete the latest record from the database.
- Delete a specific record by entering its ID.
- Clear all records from the database.
- View the entire database in a table format.
- Logout option to return to normal view.

## Technologies Used

- **Python 3.8+**
- **Streamlit** for the web interface
- **OpenAI GPT-4o** for generating material and grading
- **SQLite** for local data storage
- **PyMuPDF (fitz)** for PDF text extraction
- **python-dotenv** for managing API keys securely

## Project Structure

document-analyzer/
├── app.py                     # Main Streamlit app
├── openai_utils.py            # Teaching material and grading logic using OpenAI
├── grading_utils.py           # PDF text extraction
├── database.py                # SQLite database operations
├── students.db                # Generated SQLite database (created at runtime)
├── .env                       # API key (not checked into version control)
├── requirements.txt           # List of dependencies

## Setup Instructions

1. **Clone the repository**  

git clone 
cd document-analyzer

2. **Create and activate a virtual environment**  

python3 -m venv venv
source venv/bin/activate

3. **Install dependencies**  

pip install -r requirements.txt

4. **Set up your OpenAI API key**  
Create a `.env` file in the root directory and add:

OPENAI_API_KEY=your-openai-api-key

5. **Run the application**  

streamlit run app.py

## Requirements

See `requirements.txt`:

streamlit
openai>=1.0.0
python-dotenv
PyMuPDF
pandas

## License

This project is made by SHIVAM GOYAL (BUID:U35920740) with the help of ChatGPT
