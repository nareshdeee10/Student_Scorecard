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

# --- Hardcoded User Database (Replace with actual database lookup) ---
USERS = {
    "admin": {"password": "adminpass", "role": "admin"},
    "user_a": {"password": "userpass", "role": "regular"},
}

# ==================== SIDEBAR ====================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/trophy.png", width=100)
    st.title("ABC International School")
    st.markdown("### Academic Results 2024 - 2025")
    st.info("Public dashboard + secure personal rank card")

# ... (Authentication, Functions, and Login Form sections remain the same) ...

# Hide sidebar pages based on role if authenticated
if st.session_state.authenticated:
    
    # Hide pages that don't match the user's role
    st.markdown(
        f"""
        <style>
        .css-1f9p674 {{  /* Target the element that holds the sidebar links */
            display: {'none' if st.session_state.role != 'admin' else 'block'};
        }}
        .css-1f9p674:nth-child(2) {{ 
            display: {'none' if st.session_state.role != 'student' else 'block'};
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    # After a successful login, you can use a custom function to redirect/go to a specific page
    if st.session_state.role == "admin":
        st.experimental_set_query_params(page=["1_Admin_Dashboard"]) # For automatic redirection
        st.info("Welcome Admin! Please use the sidebar to navigate.")
    elif st.session_state.role == "student":
        st.experimental_set_query_params(page=["2_Student_View"]) # For automatic redirection
        st.info("Welcome Student! Please use the sidebar to navigate.")

else:
    # Hide all sidebar navigation if not authenticated
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] {
            display: none
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
# ==================== FOOTER ====================
st.markdown("---")
st.markdown("<p style='text-align:center; color:#888;'>© 2025 ABC International School • Powered by Streamlit</p>", unsafe_allow_html=True)
