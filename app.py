

import streamlit as st
import LoginPage
import ForgetPassword
import SignUp
import Home
import importlib.util
import sys
from pathlib import Path

# Add the pages directory to sys.path
pages_dir = Path(__file__).parent / 'pages'
sys.path.append(str(pages_dir))

# Import the MANAGE DATA page
manage_data_path = pages_dir / "🏷MANAGE DATA.py"
spec = importlib.util.spec_from_file_location("manage_data", manage_data_path)
manage_data = importlib.util.module_from_spec(spec)
sys.modules["manage_data"] = manage_data
spec.loader.exec_module(manage_data)

if "page" not in st.session_state:
    st.session_state["page"] = "LoginPage"

page = st.session_state["page"]

# Set page configuration dynamically
if page in ["LoginPage", "SignUp", "ForgetPassword"]:
    st.set_page_config(page_title="ATP Dashboard", page_icon="📘", layout="centered")
else:
    st.set_page_config(page_title="ATP Dashboard", page_icon="📘", layout="wide")

# Hide sidebar on login page
if page != "LoginPage":
    # Set the sidebar title based on user role or fullname
    if "fullname" in st.session_state:
        st.sidebar.title(st.session_state["fullname"])
    elif "is_admin" in st.session_state and st.session_state["is_admin"]:
        st.sidebar.title("Admin")
    else:
        st.sidebar.title("User")

# Render the appropriate page
if page == "LoginPage":
    LoginPage.main()
elif page == "ForgetPassword":
    ForgetPassword.main()
elif page == "SignUp":
    SignUp.main()
elif page == "Home":
    Home.main()
elif page == "MANAGE DATA":
    manage_data.main()

