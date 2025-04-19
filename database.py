import sqlite3

# Function to create a database connection
# Returns a connection object to the SQLite database
def connect_db():
    return sqlite3.connect("students.db")

# Function to initialize the database structure
# Creates the students table if it doesn't already exist
def create_students_table():
    # Establish database connection
    conn = connect_db()
    cursor = conn.cursor()
    
    # SQL to create table with defined columns if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique identifier for each record
            teacher_name TEXT,                     -- Name of the teacher
            teacher_email TEXT,                    -- Email of the teacher
            student_name TEXT,                     -- Name of the student
            grade TEXT,                            -- Letter grade (A-F)
            marks INTEGER,                         -- Numeric score (0-100)
            remarks TEXT                           -- Feedback comments
        )
    ''')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()

# Function to add a new record to the database
# Inserts student assignment data with grade information
def insert_record(teacher_name, teacher_email, student_name, grade, marks, remarks):
    # Debug prints to console
    print(">>> Inserting into DB")
    print("Teacher:", teacher_name)
    print("Student:", student_name)
    print("Grade:", grade, "Marks:", marks)
    
    # Establish database connection
    conn = connect_db()
    cursor = conn.cursor()
    
    # SQL to insert new record with provided values
    # Using parameterized query to prevent SQL injection
    cursor.execute('''
        INSERT INTO students (teacher_name, teacher_email, student_name, grade, marks, remarks)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (teacher_name, teacher_email, student_name, grade, marks, remarks))
    
    # Commit changes and close connection
    conn.commit()
    conn.close()

# Function to delete the most recently added record
# Removes the record with the highest ID from the database
def delete_latest_record():
    # Establish database connection
    conn = connect_db()
    cursor = conn.cursor()
    
    # SQL to delete the record with the maximum ID value
    cursor.execute('''
        DELETE FROM students
        WHERE id = (SELECT MAX(id) FROM students)
    ''')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()

# Function to delete a specific record by its ID
# Removes a single record identified by the provided ID
def delete_record_by_id(record_id):
    # Establish database connection
    conn = connect_db()
    cursor = conn.cursor()
    
    # SQL to delete record with matching ID
    # Using parameterized query for security
    cursor.execute('DELETE FROM students WHERE id = ?', (record_id,))
    
    # Commit changes and close connection
    conn.commit()
    conn.close()

# Function to clear all records from the table
# Removes all data while keeping the table structure
def clear_students_table():
    # Establish database connection
    conn = connect_db()
    cursor = conn.cursor()
    
    # SQL to delete all records from the table
    cursor.execute('DELETE FROM students')
    
    # Commit changes and close connection
    conn.commit()
    conn.close()

# Function to retrieve all records from the database
# Returns a list of all rows in the students table
def get_all_records():
    # Establish database connection
    conn = connect_db()
    cursor = conn.cursor()
    
    # SQL to select all records
    cursor.execute('SELECT * FROM students')
    
    # Fetch all results as a list of tuples
    rows = cursor.fetchall()
    
    # Close connection and return data
    conn.close()
    return rows
