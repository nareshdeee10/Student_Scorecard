import streamlit as st

# --- Authentication and Role Check ---
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.stop() 
    
# Important: Check for the 'student' role
if st.session_state.role != "student": 
    st.warning("❌ Access Denied: You must be a **Student** to view this page.")
    st.stop()
    
# --- Student Page Content ---
st.title("📚 Student Portal")
# ... your student specific content
