import sqlite3

def connect_db():
    return sqlite3.connect("students.db")

def create_students_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            teacher_name TEXT,
            teacher_email TEXT,
            student_name TEXT,
            grade TEXT,
            marks INTEGER,
            remarks TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_record(teacher_name, teacher_email, student_name, grade, marks, remarks):
    print(">>> Inserting into DB")
    print("Teacher:", teacher_name)
    print("Student:", student_name)
    print("Grade:", grade, "Marks:", marks)
    
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO students (teacher_name, teacher_email, student_name, grade, marks, remarks)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (teacher_name, teacher_email, student_name, grade, marks, remarks))
    conn.commit()
    conn.close()

def delete_latest_record():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM students
        WHERE id = (SELECT MAX(id) FROM students)
    ''')
    conn.commit()
    conn.close()

def delete_record_by_id(record_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()

def clear_students_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM students')
    conn.commit()
    conn.close()

def get_all_records():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students')
    rows = cursor.fetchall()
    conn.close()
    return rows