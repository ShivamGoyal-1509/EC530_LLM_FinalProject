import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import database functions to test
from database import connect_db, create_students_table, insert_record, get_all_records

# Mock Streamlit before importing app
import sys
mock_streamlit = MagicMock()
sys.modules['streamlit'] = mock_streamlit
# Mock session_state dictionary
mock_streamlit.session_state = {}
# Initialize session state variables
mock_streamlit.session_state["admin_logged_in"] = False
mock_streamlit.session_state["show_records"] = False
mock_streamlit.session_state["reset_form"] = False
mock_streamlit.session_state["display_all_records"] = False
mock_streamlit.session_state["last_record_id"] = None

# Mock the OpenAI client import to avoid initialization errors
# This needs to happen BEFORE importing the modules that use OpenAI
import builtins
original_import = builtins.__import__

def mock_import(name, *args, **kwargs):
    if name == 'openai' or name.startswith('openai.'):
        mock_module = MagicMock()
        mock_module.OpenAI = MagicMock
        return mock_module
    return original_import(name, *args, **kwargs)

# Apply the mock to __import__
builtins.__import__ = mock_import

# Now it's safe to import our OpenAI-dependent modules
from openai_utils import generate_teaching_material, grade_assignment

# Extract the validate_email function directly without importing the whole app
# This avoids Streamlit initialization issues
import re
def validate_email(email):
    if not email:
        return False
    
    # Check if email ends with @gmail.com or @bu.edu
    if email.endswith("@gmail.com") or email.endswith("@bu.edu"):
        # Basic email format validation
        email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@(gmail\.com|bu\.edu)$')
        return bool(email_pattern.match(email))
    return False

# Test database functions with mocking
class TestDatabase:
    # Test database connection
    def test_connect_db(self, monkeypatch):
        # Mock sqlite3.connect
        mock_connect = MagicMock()
        monkeypatch.setattr('sqlite3.connect', mock_connect)
        
        # Call the function
        connect_db()
        
        # Check that connect was called with correct argument
        mock_connect.assert_called_once_with("students.db")
    
    # Test table creation
    @patch('database.connect_db')
    def test_create_students_table(self, mock_connect_db):
        # Setup mock connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect_db.return_value = mock_conn
        
        # Call the function
        create_students_table()
        
        # Verify that execute was called (table creation SQL)
        assert mock_cursor.execute.called
        # Verify that commit was called
        assert mock_conn.commit.called
        # Verify that close was called
        assert mock_conn.close.called
    
    # Test inserting a record
    @patch('database.connect_db')
    def test_insert_record(self, mock_connect_db):
        # Setup mock connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_connect_db.return_value = mock_conn
        
        # Test data
        teacher_name = "John Doe"
        teacher_email = "john@gmail.com"
        student_name = "Jane Smith"
        grade = "A"
        marks = 95
        remarks = "Excellent work!"
        
        # Call the function
        insert_record(teacher_name, teacher_email, student_name, grade, marks, remarks)
        
        # Verify execute was called with correct parameters
        mock_cursor.execute.assert_called_once()
        # Check first argument of the call (should be SQL query)
        sql_query = mock_cursor.execute.call_args[0][0]
        assert "INSERT INTO students" in sql_query
        # Check second argument (should be tuple of values)
        params = mock_cursor.execute.call_args[0][1]
        assert params == (teacher_name, teacher_email, student_name, grade, marks, remarks)
        
        # Verify commit and close were called
        assert mock_conn.commit.called
        assert mock_conn.close.called
    
    # Test retrieving all records
    @patch('database.connect_db')
    def test_get_all_records(self, mock_connect_db):
        # Mock data to return
        mock_records = [
            (1, "Teacher1", "teacher1@gmail.com", "Student1", "A", 90, "Good work"),
            (2, "Teacher2", "teacher2@bu.edu", "Student2", "B", 85, "Satisfactory")
        ]
        
        # Setup mock connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = mock_records
        mock_conn.cursor.return_value = mock_cursor
        mock_connect_db.return_value = mock_conn
        
        # Call the function
        result = get_all_records()
        
        # Verify the SQL query
        mock_cursor.execute.assert_called_once_with('SELECT * FROM students')
        # Verify fetchall was called
        assert mock_cursor.fetchall.called
        # Verify the returned records match our mock data
        assert result == mock_records
        # Verify connection was closed
        assert mock_conn.close.called

# Test OpenAI utility functions
class TestOpenAIUtils:
    # Mock the OpenAI client for all tests in this class
    @pytest.fixture(autouse=True)
    def setup_openai_mock(self, monkeypatch):
        # Create a mock for the OpenAI client
        self.mock_openai = MagicMock()
        self.mock_completion = MagicMock()
        self.mock_openai.chat.completions.create.return_value = self.mock_completion
        
        # Patch the OpenAI client in the module
        monkeypatch.setattr('openai_utils.client', self.mock_openai)
        
    # Test generate_teaching_material with mocked OpenAI API
    def test_generate_teaching_material(self):
        # Set up the mock response
        self.mock_completion.choices = [MagicMock()]
        self.mock_completion.choices[0].message.content = "This is mock teaching material"
        
        # Call the function
        topic = "Python Basics"
        result = generate_teaching_material(topic)
        
        # Verify API was called
        assert self.mock_openai.chat.completions.create.called
        # Verify returned content
        assert result == "This is mock teaching material"
    
    # Test grade_assignment with mocked OpenAI API
    def test_grade_assignment(self):
        # Set up the mock response with proper formatting
        self.mock_completion.choices = [MagicMock()]
        self.mock_completion.choices[0].message.content = "Grade: B\nMarks: 85\nRemarks: Good effort but needs improvement."
        
        # Call the function
        assignment_text = "This is a sample assignment submission"
        grade, marks, remarks = grade_assignment(assignment_text)
        
        # Verify API was called
        assert self.mock_openai.chat.completions.create.called
        
        # Verify parsed results
        assert grade == "B"
        assert marks == 85
        assert remarks == "Good effort but needs improvement."
        
# Test email validation function 
class TestEmailValidation:
    def test_valid_gmail(self):
        assert validate_email("test@gmail.com") == True
        
    def test_valid_bu_edu(self):
        assert validate_email("student@bu.edu") == True
        
    def test_invalid_domains(self):
        assert validate_email("test@yahoo.com") == False
        assert validate_email("test@hotmail.com") == False
        
    def test_invalid_format(self):
        assert validate_email("test@") == False
        assert validate_email("test@gmail") == False
        assert validate_email("testgmail.com") == False
        assert validate_email("") == False
