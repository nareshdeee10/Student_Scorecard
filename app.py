import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ====================== CONFIG ======================
st.set_page_config(
    page_title="ABC School - Result Dashboard 2025",
    page_icon="trophy",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .big-font {font-size: 50px !important; font-weight: bold; text-align: center; color: #1e3d59;}
    .metric-card {background: linear-gradient(90deg, #667eea, #764ba2); padding: 20px; border-radius: 15px; color: white;}
    .topper-card {background: #fff3e0; padding: 15px; border-radius: 12px; border-left: 6px solid #ff9800;}
    .stTabs [data-baseweb="tab"] {font-size: 18px; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# ====================== DATA ======================
@st.cache_data
def load_results():
    data = {
        "Roll No": ["S1001","S1002","S1003","S1004","S1005","S1006","S1007","S1008","S1009","S1010"],
        "Name": ["Aarav Sharma","Isha Patel","Rohan Kumar","Priya Singh","Vikram Mehta",
                 "Ananya Gupta","Arjun Reddy","Saanvi Joshi","Reyansh Verma","Diya Nair"],
        "Class": ["10th"]*10,
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
    df["Percentage"] = df["Total"] / 5
    df = df.sort_values("Percentage", ascending=False).reset_index(drop=True)
    df["Rank"] = df.index + 1
    return df

df = load_results()

# ====================== SIDEBAR ======================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/trophy.png", width=100)
    st.title("ABC International School")
    st.markdown("### Annual Exam Results 2025")
    st.markdown("---")
    st.info("View overall performance or check your personal rank card below")

# ====================== MAIN DASHBOARD ======================
st.markdown("<p class='big-font'>Result Dashboard 2025</p>", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Overall Performance", "Toppers List", "My Rank Card"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Students", len(df))
    with col2:
        st.metric("Class Average", f"{df['Percentage'].mean():.2f}%")
    with col3:
        st.metric("Highest Score", f"{df['Percentage'].max():.2f}%")
    with col4:
        st.metric("Pass % (above 33%)", f"{(df['Percentage'] >= 33).mean()*100:.1f}%")

    col_a, col_b st.columns(2)
    with col_a:
        fig = px.bar(df.head(10), x="Name", y="Percentage", title="Top 10 Students",
                     color="Percentage", color_continuous_scale="Viridis")
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        subject_avg = df[["Maths","Science","English","Social","Hindi"]].mean()
        fig2 = px.pie(values=subject_avg.values, names=subject_avg.index,
                      title="Average Marks by Subject", color_discrete_sequence=px.colors.sequential.Plasma)
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.markdown("### Top 10 Students - 2025")
    top10 = df.head(10)[["Rank","Roll No","Name","Total","Percentage"]]
    top10["Percentage"] = top10["Percentage"].round(2)
    st.dataframe(top10.style.background_gradient(cmap="Blues"), use_container_width=True)

    for _, row in df.head(5).iterrows():
        with st.container():
            st.markdown(f"""
            <div class="topper-card">
                <h3>trophy Rank {int(row['Rank'])}: {row['Name']}</h3>
                <p><strong>Roll No:</strong> {row['Roll No']} | <strong>Total:</strong> {int(row['Total'])}/500 | 
                   <strong>Percentage:</strong> {row['Percentage']:.2f}% badge</p>
            </div><br>
            """, unsafe_allow_html=True)

with tab3:
    st.markdown("### Your Personal Rank Card")
    c1, c2 = st.columns(2)
    with c1:
        roll = st.text_input("Enter Roll Number", placeholder="e.g., S1001")
    with c2:
        auth = st.text_input("Password or DOB (YYYY-MM-DD)", type="password", placeholder="e.g., aarav123")

    if st.button("Generate My Rank Card", type="primary", use_container_width=True):
        if not roll or not auth:
            st.error("Please fill both fields")
        else:
            student = df[df["Roll No"].str.upper() == roll.strip().upper()]
            if student.empty:
                st.error("Roll Number not found!")
            elif auth != student.iloc[0]["Password"] and auth != student.iloc[0]["DOB"]:
                st.error("Incorrect Password or Date of Birth!")
            else:
                s = student.iloc[0]
                st.balloons()
                st.success(f"Welcome back, {s['Name']}! Here is your result:")

                # Beautiful Rank Card
                st.markdown(f"""
                <div style="background:linear-gradient(135deg,#667eea,#764ba2); padding:30px; border-radius:20px; color:white; text-align:center; box-shadow:0 10px 30px rgba(0,0,0,0.3);">
                    <h1>{s['Name']}</h1>
                    <h3>Class: {s['Class']} | Roll No: {s['Roll No']}</h3>
                    <h1 style="font-size:60px; color:#ffeb3b; text-shadow:2px 2px 10px black;">Rank {int(s['Rank'])}</h1>
                    <h2>Total: {int(s['Total'])}/500 ({s['Percentage']:.2f}%)</h2>
                </div>
                """, unsafe_allow_html=True)

                colx, coly, colz = st.columns(3)
                colx.metric("Maths", f"{s['Maths']}/100")
                coly.metric("Science", f"{s['Science']}/100")
                colz.metric("English", f"{s['English']}/100")
                cola, colb = st.columns(2)
                cola.metric("Social Science", f"{s['Social']}/100")
                colb.metric("Hindi", f"{s['Hindi']}/100")

                if s['Percentage'] >= 90:
                    st.markdown("<h2 style='text-align:center; color:#4caf50;'>Grade: A1 - Outstanding! star</h2>", unsafe_allow_html=True)
                elif s['Percentage'] >= 80:
                    st.markdown("<h2 style='text-align:center; color:#8bc34a;'>Grade: A2 - Excellent! star</h2>", unsafe_allow_html=True)

                # PDF Download (simulated)
                st.download_button(
                    label="Download Rank Card as PDF",
                    data=f"Rank Card\nName: {s['Name']}\nRank: {s['Rank']}\nPercentage: {s['Percentage']:.2f}%".encode(),
                    file_name=f"RankCard_{s['Roll No']}.txt",
                    mime="text/plain"
                )
                st.info("Note: For real PDF, use browser print → Save as PDF")

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center; color:#666;'>© 2025 ABC International School | Made with Streamlit</p>", unsafe_allow_html=True)
