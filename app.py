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
    
# --- Initialization ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.username = None

# --- Functions ---
def authenticate(username, password):
    if username in USERS and USERS[username]['password'] == password:
        st.session_state.authenticated = True
        st.session_state.role = USERS[username]['role']
        st.session_state.username = username
        st.success(f"Welcome, {username}!")
    else:
        st.error("Invalid username or password.")

def logout():
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.username = None
    st.experimental_rerun() # Rerun to show the login page immediately

def show_login_page():
    st.title("🔐 Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        authenticate(username, password)

def show_admin_page():
    st.title("👑 Admin Dashboard")
    st.write(f"Hello, **{st.session_state.username}**! You have **admin** privileges.")
    st.button("Logout", on_click=logout)
    st.info("Admin-only content goes here...")

def show_regular_page():
    st.title("👤 Regular User Portal")
    st.write(f"Hello, **{st.session_state.username}**! You have **regular** privileges.")
    st.button("Logout", on_click=logout)
    st.info("Regular user content goes here...")
    
# --- Main App Logic ---
if not st.session_state.authenticated:
    show_login_page()
else:
    # Use st.sidebar for the logout button in a multi-page setup
    if st.session_state.role == "admin":
        show_admin_page()
    elif st.session_state.role == "regular":
        show_regular_page()
    else:
        st.error("Unknown user role.")
        logout()
# ==================== FOOTER ====================
st.markdown("---")
st.markdown("<p style='text-align:center; color:#888;'>© 2025 ABC International School • Powered by Streamlit</p>", unsafe_allow_html=True)
