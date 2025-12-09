import streamlit as st

# --- Hardcoded User Database (Update this for your needs) ---
USERS = {
    "admin": {"password": "adminpass", "role": "admin"},
    "student_a": {"password": "studentpass", "role": "student"},
}

# --- Configuration ---
st.set_page_config(
    page_title="Secure Streamlit App",
    page_icon="🔒"
)

# --- Initialization Block (Critical for fixing the AttributeError!) ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'role' not in st.session_state:
    st.session_state.role = None
if 'username' not in st.session_state:
    st.session_state.username = None

# --- Functions ---
def authenticate(username, password):
    """Checks credentials and updates session state."""
    if username in USERS and USERS[username]['password'] == password:
        st.session_state.authenticated = True
        st.session_state.role = USERS[username]['role']
        st.session_state.username = username
        st.success(f"Login successful. Welcome, {username}!")
        # Use rerun to refresh the app state and apply navigation/hiding logic
        st.rerun() 
    else:
        st.error("Invalid username or password.")

def logout():
    """Resets session state and returns to the login screen."""
    st.session_state.authenticated = False
    st.session_state.role = None
    st.session_state.username = None
    st.rerun()

# --- Main App Logic ---

if st.session_state.authenticated:
    
    # 1. Display Logout in Sidebar
    with st.sidebar:
        st.write(f"Logged in as: **{st.session_state.username}** ({st.session_state.role})")
        st.button("Logout", on_click=logout)
        
    st.title(f"Welcome, {st.session_state.username}! 👋")
    st.info("Your designated page is displayed automatically. Use the sidebar for navigation (if other pages are available).")

    # 2. Conditional Redirection (Autonavigation after login)
    if st.session_state.role == "admin":
        # Redirect to the Admin page
        st.experimental_set_query_params(page=["1_Admin_Dashboard"])
    elif st.session_state.role == "student":
        # Redirect to the Student page
        st.experimental_set_query_params(page=["2_Student_View"])

    # 3. CSS to conditionally hide irrelevant pages from the sidebar
    # Note: Streamlit pages are numbered 1, 2, 3... 
    # This CSS uses nth-child to hide the wrong page for the current role
    st.markdown(
        f"""
        <style>
        /* Target the sidebar navigation links container */
        .st-emotion-cache-1f9p674 {{ 
            /* Hide Admin Page (1st link) if user is NOT admin */
            display: {'none' if st.session_state.role != 'admin' else 'block'} !important;
        }}
        .st-emotion-cache-1f9p674 + .st-emotion-cache-1f9p674 {{
            /* Hide Student Page (2nd link) if user is NOT student */
            display: {'none' if st.session_state.role != 'student' else 'block'} !important;
        }}
        /* If you have more pages, you'll need more specific CSS */
        </style>
        """,
        unsafe_allow_html=True,
    )
    
else:
    # Display Login Form if not authenticated
    st.title("🔐 Secure Login Portal")
    
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            authenticate(username, password)

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
