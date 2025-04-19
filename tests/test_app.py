import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import functions to test
from database import connect_db, create_students_table, insert_record, get_all_records
from openai_utils import generate_teaching_material, grade_assignment

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
