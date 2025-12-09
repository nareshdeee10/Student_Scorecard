import streamlit as st
import pandas as pd

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="ABC School • Results 2025",
    page_icon="icon.png",
    layout="wide"
)

# ==================== CSS ====================
st.markdown("""
<style>
    .big-font {font-size: 50px !important; font-weight: bold; text-align: center; color: #1e3d59;}
    .sub-font {font-size: 24px; text-align: center; color: #f47b20;}
    .topper-card {
        background: linear-gradient(90deg, #fff3e0, #ffe0b2);
        padding: 20px; border-radius: 15px; margin: 15px 0;
        border-left: 8px solid #ff9800; box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    .rank-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white; padding: 40px; border-radius: 20px;
        text-align: center; box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# ==================== DATA (with Class column fixed) ====================
@st.cache_data
def load_results():
    data = {
        "Roll No": ["S1001","S1002","S1003","S1004","S1005","S1006","S1007","S1008","S1009","S1010"],
        "Name": ["Aarav Sharma","Isha Patel","Rohan Kumar","Priya Singh","Vikram Mehta",
                 "Ananya Gupta","Arjun Reddy","Saanvi Joshi","Reyansh Verma","Diya Nair"],
        "Class": ["10th A"]*10,  # Fixed: added Class column
        "Maths": [95,88,72,91,85,93,79,96,82,89],
        "Science": [92,85,78,89,80,90,83,94,77,91],
        "English": [88,90,82,87,92,86,88,91,85,93],
        "Social": [90,87,75,93,88,89,81,95,79,87],
        "Hindi": [93,91,80,85,90,92,84,93,88,90],
        "DOB": ["2009-05-15","2009-08-22","2009-03-10","2009-11-30","2009-07-18",
                "2009-01-12","2009-09-05","2009-04-20","2009-06-30","2009-12-01"],
        "Password": ["aarav123","isha123","rohan123","priya123","vikram123",
                     "ananya123","arjun123","saanvi123","reyansh123","diya123"]
    }
    df = pd.DataFrame(data)
    df["Total"] = df[["Maths","Science","English","Social","Hindi"]].sum(axis=1)
    df["Percentage"] = round(df["Total"] / 5, 2)
    df = df.sort_values("Percentage", ascending=False).reset_index(drop=True)
    df["Rank"] = df.index + 1
    return df

df = load_results()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/trophy.png", width=100)
    st.title("ABC International School")
    st.markdown("### Annual Results 2025")
    st.info("Public dashboard + secure personal rank card")

# ==================== HEADER ====================
st.markdown('<p class="big-font">Result Dashboard 2025</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-font">Class 10th • Annual Examination</p>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Overall Performance", "Toppers List", "My Rank Card"])

# ==================== TAB 1 ====================
with tab1:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Students", len(df))
    c2.metric("Class Average", f"{df['Percentage'].mean():.2f}%")
    c3.metric("Highest %", f"{df['Percentage'].max():.2f}%")
    c4.metric("Pass Rate", f"{(df['Percentage'] >= 33).mean()*100:.1f}%")

    st.markdown("#### Top 10 Students – Percentage")
    chart_df = df.head(10)[["Name", "Percentage"]].set_index("Name")
    st.bar_chart(chart_df, use_container_width=True)

    st.markdown("#### Subject-wise Average Marks")
    subj_avg = df[["Maths","Science","English","Social","Hindi"]].mean().round(1)
    st.bar_chart(subj_avg, use_container_width=True)

# ==================== TAB 2 ====================
with tab2:
    st.markdown("### Top 10 Students")
    top10 = df.head(10)[["Rank", "Roll No", "Name", "Total", "Percentage"]].copy()
    top10["Percentage"] = top10["Percentage"].astype(str) + " %"
    st.dataframe(top10, use_container_width=True, hide_index=False)

    st.markdown("### Our Shining Stars!")
    for _, row in df.head(5).iterrows():
        st.markdown(f"""
        <div class="topper-card">
            <h3>Rank {int(row['Rank'])} → {row['Name']}</h3>
            <p><b>Roll No:</b> {row['Roll No']} | <b>Total:</b> {int(row['Total'])}/500 | <b>Percentage:</b> {row['Percentage']}%</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== TAB 3 – My Rank Card ====================
with tab3:
    st.markdown("### Enter Details to View Your Rank Card")
    col1, col2 = st.columns(2)
    with col1:
        roll = st.text_input("Roll Number", placeholder="e.g., S1001")
    with col2:
        auth = st.text_input("Password or DOB (YYYY-MM-DD)", type="password", placeholder="e.g., aarav123")

    if st.button("Show My Rank Card", type="primary", use_container_width=True):
        if not roll or not auth:
            st.error("Please fill both fields")
        else:
            student = df[df["Roll No"].str.upper() == roll.strip().upper()]
            if student.empty:
                st.error("Roll Number not found!")
            elif auth not in [student.iloc[0]["Password"], student.iloc[0]["DOB"]]:
                st.error("Incorrect Password or Date of Birth")
            else:
                s = student.iloc[0]
                st.balloons()

                # Beautiful Rank Card
                st.markdown(f"""
                <div class="rank-card">
                    <h1 style="margin:10px 0;">{s['Name']}</h1>
                    <p style="font-size:22px; margin:5px;">Class {s['Class']} | Roll No: {s['Roll No']}</p>
                    <h1 style="font-size:90px; color:#ffeb3b; margin:20px; text-shadow:4px 4px 15px black;">
                        Rank {int(s['Rank'])}
                    </h1>
                    <h2>{int(s['Total'])} / 500  ({s['Percentage']}%)</h2>
                </div><br>
                """, unsafe_allow_html=True)

                # Subject marks
                cols = st.columns(5)
                subjects = ["Maths","Science","English","Social","Hindi"]
                for col, sub in zip(cols, subjects):
                    col.metric(sub, f"{int(s[sub])}/100")

                # Grade
                perc = s['Percentage']
                grade = "A1" if perc >= 90 else "A2" if perc >= 80 else "B1" if perc >= 70 else "B2" if perc >= 60 else "C"
                st.markdown(f"<h2 style='text-align:center; color:#4caf50;'>Overall Grade: {grade}</h2>", unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("<p style='text-align:center; color:#888;'>© 2025 ABC International School • Powered by Streamlit</p>", unsafe_allow_html=True)
