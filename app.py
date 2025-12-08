import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Student Rank Card", page_icon="🎓", layout="centered")

# Custom CSS for beautiful rank card
st.markdown("""
<style>
<style>
    .main-header {
        font-size: 42px;
        color: #1e3d59;
        text-align: center;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .sub-header {
        font-size: 20px;
        color: #f47b20;
        text-align: center;
        margin-bottom: 30px;
    }
    .rank-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        color: white;
        max-width: 700px;
        margin: 20px auto;
    }
    .student-name {
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        margin: 10px 0;
        color: #fff;
    }
    .info-row {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        font-size: 18px;
    }
    .label {
        font-weight: bold;
        color: #a0e7ff;
    }
    .rank-highlight {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        color: #ffeb3b;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.5);
        margin: 20px 0;
    }
    .grade-A { color: #4caf50; font-weight: bold; }
    .grade-B { color: #ff9800; font-weight: bold; }
    .grade-C { color: #f44336; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# Sample student data (in real app, load from CSV, database or Google Sheets)
@st.cache_data
def load_data():
    data = {
        "Roll No": ["S1001", "S1002", "S1003", "S1004", "S1005"],
        "Name": ["Aarav Sharma", "Isha Patel", "Rohan Kumar", "Priya Singh", "Vikram Mehta"],
        "Class": ["10th", "10th", "10th", "10th", "10th"],
        "Maths": [95, 88, 72, 91, 85],
        "Science": [92, 85, 78, 89, 80],
        "English": [88, 90, 82, 87, 92],
        "Social": [90, 87, 75, 93, 88],
        "Hindi": [93, 91, 80, 85, 90],
        "DOB": ["2009-05-15", "2009-08-22", "2009-03-10", "2009-11-30", "2009-07-18"],  # for verification
        "Password": ["aarav123", "isha123", "rohan123", "priya123", "vikram123"]  # simple auth
    }
    df = pd.DataFrame(data)
    df["Total"] = df[["Maths", "Science", "English", "Social", "Hindi"]].sum(axis=1)
    df["Percentage"] = df["Total"] / 5
    df = df.sort_values(by="Percentage", ascending=False).reset_index(drop=True)
    df["Rank"] = df.index + 1
    return df

# Load data
df = load_data()

# Title
st.markdown("<h1 class='main-header'>🏫 ABC International School</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Annual Examination 2025 - Rank Card</p>", unsafe_allow_html=True)

st.markdown("### 🔐 Enter Your Credentials to View Rank Card")

col1, col2 = st.columns(2)
with col1:
    roll_no = st.text_input("Roll Number", placeholder="e.g., S1001")
with col2:
    password = st.text_input("Password / DOB (YYYY-MM-DD)", type="password", placeholder="e.g., aarav123 or 2009-05-15")

if st.button("View My Rank Card", type="primary", use_container_width=True):
    if not roll_no or not password:
        st.error("Please enter both Roll Number and Password/DOB")
    else:
        student = df[df["Roll No"].astype(str).str.upper() == roll_no.strip().upper()]
        
        if student.empty:
            st.error("❌ Roll Number not found!")
        else:
            student = student.iloc[0]
            # Authentication
            if password == student["Password"] or password == student["DOB"]:
                # Success - Show Rank Card
                st.markdown(f"<div class='rank-card'>", unsafe_allow_html=True)
                st.markdown(f"<div class='student-name'>{student['Name']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='text-align:center; font-size:20px;'>{student['Class']} | Roll No: {student['Roll No']}</div>", unsafe_allow_html=True)

                st.markdown("<h2 style='text-align:center; margin:20px 0;'>Subject-wise Marks</h2>", unsafe_allow_html=True)

                subjects = ["Maths", "Science", "English", "Social", "Hindi"]
                for sub in subjects:
                    marks = student[sub]
                    st.markdown(f"<div class='info-row'><span class='label'>{sub}</span><span>{marks}/100</span></div>", unsafe_allow_html=True)

                st.markdown("<hr style='border-color:#fff4'>", unsafe_allow_html=True)

                st.markdown(f"<div class='info-row'><span class='label'>Total Marks</span><span>{int(student['Total'])} / 500</span></div>", unsafe_allow_html=True)
                st.markdown(f"<div class='info-row'><span class='label'>Percentage</span><span>{student['Percentage']:.2f}%</span></div>", unsafe_allow_html=True)

                # Grade logic
                perc = student['Percentage']
                if perc >= 90:
                    grade = "A1"
                    grade_class = "grade-A"
                elif perc >= 80:
                    grade = "A2"
                    grade_class = "grade-A"
                elif perc >= 70:
                    grade = "B1"
                    grade_class = "grade-B"
                elif perc >= 60:
                    grade = "B2"
                    grade_class = "grade-B"
                else:
                    grade = "C1 or Below"
                    grade_class = "grade-C"

                st.markdown(f"<div class='info-row'><span class='label'>Grade</span><span class='{grade_class}'>{grade}</span></div>", unsafe_allow_html=True)

                st.markdown(f"<div class='rank-highlight'>Rank: {int(student['Rank'])}</div>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

                st.success("🎉 Congratulations! Keep up the great work!")
                st.balloons()
            else:
                st.error("Incorrect Password or Date of Birth!")

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center; color:#666;'>This is a secure online rank card portal.<br>Do not share your credentials with anyone.</p>", unsafe_allow_html=True)
