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
- **GitHub Actions** for continuous integration and testing

## Project Structure
```
document-analyzer/
  ├── app.py                      # Main Streamlit app
  ├── openai_utils.py             # Teaching material and grading logic using OpenAI
  ├── grading_utils.py            # PDF text extraction
  ├── database.py                 # SQLite database operations
  ├── students.db                 # Generated SQLite database (created at runtime)
  ├── .env                        # API key (not checked into version control)
  ├── requirements.txt            # List of dependencies
  ├── tests/                      # Test directory
  │   └── test_app.py             # Unit tests for app functionality
  └── .github/                    # GitHub configuration
      └── workflows/              # GitHub Actions workflows
          └── streamlit-app-test.yml  # CI workflow definition
```

## Setup Instructions

1. **Clone the repository**  
```bash
git clone https://github.com/yourusername/document-analyzer.git
cd document-analyzer
```

2. **Create and activate a virtual environment**  
```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. **Install dependencies**  
```bash
pip install -r requirements.txt
```

4. **Set up your OpenAI API key**  
Create a `.env` file in the root directory and add:
```
OPENAI_API_KEY=your-openai-api-key
```

5. **Run the application**  
```bash
streamlit run app.py
```

## Continuous Integration with GitHub Actions

This project uses GitHub Actions for automated testing and code quality checks. The workflow:

1. **Linting**: Checks code quality and applies formatting with flake8 and black
2. **Unit Testing**: Runs all tests in the `tests/` directory using pytest
3. **Streamlit Testing**: Performs basic smoke tests on the Streamlit app

### Running Tests Locally

To run the tests on your local machine:

```bash
# Install test dependencies
pip install pytest pytest-mock

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test class
pytest tests/test_app.py::TestDatabase
```

### GitHub Actions Workflow

The workflow runs automatically on:
- Every push to the main branch
- Every pull request to the main branch
- Manual triggers from the GitHub Actions tab

To view workflow results:
1. Go to the GitHub repository
2. Click on the "Actions" tab
3. Select a workflow run to see details and logs

## Requirements

See `requirements.txt`:
```
streamlit
openai>=1.0.0
python-dotenv
PyMuPDF
pandas
pytest
pytest-mock
flake8
black
```

## License

This project is made by SHIVAM GOYAL (BUID: U35920740) with some help from ChatGPT.
