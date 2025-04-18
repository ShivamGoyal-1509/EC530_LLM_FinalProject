import streamlit as st
import tempfile
import pandas as pd
import sqlite3
import time
import re

from grading_utils import extract_text_from_pdf
from openai_utils import generate_teaching_material, grade_assignment
from database import (
    insert_record, create_students_table,
    delete_latest_record, delete_record_by_id,
    clear_students_table, get_all_records
)

st.set_page_config(page_title="Document Analyzer for Teachers", layout="wide")

# Initialize session state
if "admin_logged_in" not in st.session_state:
    st.session_state["admin_logged_in"] = False
if "show_records" not in st.session_state:
    st.session_state["show_records"] = False
if "reset_form" not in st.session_state:
    st.session_state["reset_form"] = False
if "display_all_records" not in st.session_state:
    st.session_state["display_all_records"] = False
if "last_record_id" not in st.session_state:
    st.session_state["last_record_id"] = None

create_students_table()
st.title("📚 Document Analyzer for Teachers")

# Function to validate email
def validate_email(email):
    if not email:
        return False
    
    # Check if email ends with @gmail.com or @bu.edu
    if email.endswith("@gmail.com") or email.endswith("@bu.edu"):
        # Basic email format validation
        email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@(gmail\.com|bu\.edu)$')
        return bool(email_pattern.match(email))
    return False

# Function to get the latest record
def get_latest_record():
    conn = sqlite3.connect("students.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students ORDER BY id DESC LIMIT 1")
    record = cursor.fetchone()
    conn.close()
    return record

# -------------------------------
# 🔐 Admin Login + Panel (Sidebar)
# -------------------------------
st.sidebar.header("🔐 Admin Login")

if not st.session_state["admin_logged_in"]:
    admin_user = st.sidebar.text_input("Username")
    admin_pass = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if admin_user == "admin" and admin_pass == "qwerty":
            st.session_state["admin_logged_in"] = True
            st.sidebar.success("✅ Logged in as admin")
            st.rerun()
        else:
            st.sidebar.error("❌ Invalid credentials")
else:
    st.sidebar.success("✅ Logged in as admin")
    if st.sidebar.button("Logout"):
        st.session_state["admin_logged_in"] = False
        st.rerun()

# Function to display individual record fields with full visibility
def display_single_record(record, column_names):
    if record:
        st.write("### Record Details")
        
        # Create columns for better layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**ID:** {record[0]}")
            st.write(f"**Teacher:** {record[1]}")
            st.write(f"**Email:** {record[2]}")
            st.write(f"**Student:** {record[3]}")
        
        with col2:
            st.write(f"**Grade:** {record[4]}")
            st.write(f"**Marks:** {record[5]}")
            
        # Display remarks in full width with a text area
        st.write("**Remarks:**")
        st.text_area("", record[6], height=100, disabled=True)

# Function to display dataframe with scrollable columns
def display_scrollable_dataframe(data, column_names):
    df = pd.DataFrame(data, columns=column_names)
    
    # Set the dataframe to use the full width of the page
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=False,
        column_config={
            "Remarks": st.column_config.TextColumn(
                "Remarks",
                width="large",
                help="Student remarks"
            )
        }
    )

# -------------------------------
# 🛠️ Admin Panel
# -------------------------------
if st.session_state["admin_logged_in"]:
    st.subheader("🛠️ Admin Panel")

    if st.button("🗑️ Delete Latest Record"):
        delete_latest_record()
        st.success("✅ Deleted latest record.")

    record_id = st.text_input("Enter Record ID to Delete")
    if st.button("❌ Delete Specific Record"):
        if record_id.isdigit():
            delete_record_by_id(int(record_id))
            st.success(f"✅ Deleted record with ID {record_id}.")
        else:
            st.warning("⚠️ Please enter a valid numeric ID.")

    if st.button("💣 Clear Entire Table"):
        clear_students_table()
        st.success("✅ All records deleted.")

    st.subheader("📋 All Records")
    records = get_all_records()
    if records:
        column_names = ["ID", "Teacher", "Email", "Student", "Grade", "Marks", "Remarks"]
        display_scrollable_dataframe(records, column_names)
    else:
        st.info("ℹ️ No records found.")

# -------------------------------
# 📊 View Recently Added Record
# -------------------------------
if st.session_state.get("show_records", False):
    st.subheader("📋 Recently Added Record")
    
    # Get only the latest record
    latest_record = get_latest_record()
    
    if latest_record:
        column_names = ["ID", "Teacher", "Email", "Student", "Grade", "Marks", "Remarks"]
        # Use the new function to display a single record with better formatting
        display_single_record(latest_record, column_names)
    else:
        st.info("ℹ️ No records found.")
    
    # Reset the flag after showing
    st.session_state["show_records"] = False
    
    if st.button("Continue"):
        st.session_state["reset_form"] = True
        st.rerun()

# Reset form if needed
elif st.session_state.get("reset_form", False):
    # Reset the flag
    st.session_state["reset_form"] = False
    # Continue with empty form

else:
    # -------------------------------
    # 👨‍🏫 Teacher Inputs
    # -------------------------------
    st.subheader("Enter your details")
    teacher_name = st.text_input("Name")
    teacher_email = st.text_input("Email")
    
    # Validate email format
    if teacher_email and not validate_email(teacher_email):
        st.warning("⚠️ Email must end with @gmail.com or @bu.edu")
        valid_email = False
    else:
        valid_email = True if not teacher_email else True

    # -------------------------------
    # 🚀 Action Selection
    # -------------------------------
    st.subheader("Choose an Action")
    option = st.radio("What would you like to do?", ["Upload Assignment PDF", "Generate Teaching Material with AI"])

    # -------------------------------
    # 📄 Upload & Grade Assignment
    # -------------------------------
    if option == "Upload Assignment PDF":
        student_name = st.text_input("Student Name")
        uploaded_file = st.file_uploader("Upload PDF file", type=["pdf"])

        if uploaded_file and st.button("Analyze and Grade"):
            if not teacher_name or not teacher_email or not student_name:
                st.warning("⚠️ Please enter all required fields (teacher name, email, student name).")
            elif not valid_email:
                st.warning("⚠️ Please enter a valid email ending with @gmail.com or @bu.edu")
            else:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.read())
                    file_path = tmp_file.name

                text = extract_text_from_pdf(file_path)
                grade, marks, remarks = grade_assignment(text)

                st.success(f"Grade: {grade} | Marks: {marks}")
                st.info(f"Remarks: {remarks}")

                insert_record(teacher_name, teacher_email, student_name, grade, marks, remarks)
                st.success("✅ Record saved to database.")
                
                # Set flag to show records and reset form
                st.session_state["show_records"] = True
                st.rerun()

    # -------------------------------
    # 🤖 Generate + Grade AI Material
    # -------------------------------
    elif option == "Generate Teaching Material with AI":
        topic = st.text_input("Enter topic for material generation")
        student_name = st.text_input("Student Name")
        material_generated = False

        if topic and st.button("Generate"):
            material = generate_teaching_material(topic)
            st.session_state["material"] = material
            material_generated = True

        if "material" in st.session_state:
            st.text_area("Generated Teaching Material", st.session_state["material"], height=300)

            if st.button("Grade This Material"):
                if not teacher_name or not teacher_email or not student_name:
                    st.warning("⚠️ Please enter all required fields (teacher name, email, student name).")
                elif not valid_email:
                    st.warning("⚠️ Please enter a valid email ending with @gmail.com or @bu.edu")
                else:
                    grade, marks, remarks = grade_assignment(st.session_state["material"])
                    
                    st.success(f"Grade: {grade} | Marks: {marks}")
                    st.info(f"Remarks: {remarks}")

                    insert_record(teacher_name, teacher_email, student_name, grade, marks, remarks)
                    st.success("✅ Record saved to database.")
                    
                    # Set flag to show records and reset form
                    st.session_state["show_records"] = True
                    st.rerun()

# -------------------------------
# 📊 View Student Submissions
# -------------------------------
st.sidebar.header("📊 View Submissions")

# Toggle button to show/hide records
if not st.session_state.get("display_all_records", False):
    if st.sidebar.button("📋 Show All Records"):
        st.session_state["display_all_records"] = True
        st.rerun()
else:
    if st.sidebar.button("🙈 Hide Records"):
        st.session_state["display_all_records"] = False
        st.rerun()
    
    # Only display records if the flag is set
    conn = sqlite3.connect("students.db")
    df = pd.read_sql_query("SELECT * FROM students", conn)
    conn.close()

    st.subheader("📋 All Student Submissions")
    if not df.empty:
        display_scrollable_dataframe(df.values.tolist(), df.columns.tolist())
    else:
        st.info("ℹ️ No records found.")