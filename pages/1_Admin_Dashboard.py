import streamlit as st

# --- Authentication and Role Check ---
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.stop() 
    
if st.session_state.role != "admin":
    st.warning("❌ Access Denied: You must be an **Admin** to view this page.")
    st.stop()
    
# --- Admin Page Content ---
st.title("👑 Admin Dashboard")
# ... your admin specific content
