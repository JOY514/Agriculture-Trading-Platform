import streamlit as st
import re
import mysql.connector
import base64

# Function to validate email
def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

# Function to validate password
def validate_password(password):
    return re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password)

# Save data to MySQL
def save_data_to_mysql(fullname, email, password, state, phone):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="Mirza@haziq514",
            database="agriculture"
        )
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO atpuser (fullname, emailaddress, password, state, phonenumber) 
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (fullname, email, password, state, phone))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        st.error(f"Error while connecting to MySQL: {e}")
        return False

def main():
    image_path = "data/agri1.jpg"
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <style>
            .stApp {{
                background: url("data:image/jpg;base64,{base64_image}") no-repeat center center fixed;
                background-size: cover;
            }}
            .signup-container {{
                background: rgba(0, 0, 0, 0);  /* Adjusted opacity */
                padding: 20px;
                border-radius: 10px;
                width: 100%;
                max-width: 400px;
                margin: auto;
                margin-top: 10%;
                text-align: center;
            }}
            .signup-title {{
                font-size: 32px;
                margin-bottom: 20px;
                color: white;
                text-align: center;
            }}
            .stTextInput input, .stSelectbox div {{
                color: white !important;
            }}
            .stTextInput input::placeholder, .stSelectbox div::placeholder {{
                color: white !important;
            }}
            .stTextInput label, .stSelectbox label {{
                color: white !important;
                font-weight: bold !important;
            }}
            .signup-button {{
                width: 100%;
                display: flex;
                justify-content: center;
                margin-top: 10px;
            }}
            [data-testid="stSidebar"] {{
                display: none;
            }}
            .header {{
                font-size: 32px;
                color: white;
                text-align: center;
                margin-top: 20px;
                margin-bottom: 20px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="header">COME AND JOIN OUR COMMUNITY MEMBER FOR MORE ADVENTURE!</div>', unsafe_allow_html=True)
    st.markdown('<div class="signup-container">', unsafe_allow_html=True)
    st.markdown('<div class="signup-title">Sign Up</div>', unsafe_allow_html=True)

    fullname = st.text_input("Full Name", placeholder="e.g., Ali Bin Abu", key="fullname")
    email = st.text_input("Email Address", placeholder="e.g., abc@gmail.com", key="email")
    password = st.text_input("Password", type="password", placeholder="e.g., Abc12345", key="password")
    confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
    
    state = st.selectbox("State", [
        "Johor", "Kedah", "Kelantan", "Malacca", "Negeri Sembilan", "Pahang", "Penang", 
        "Perak", "Perlis", "Sabah", "Sarawak", "Selangor", "Terengganu", 
        "Kuala Lumpur", "Putrajaya", "Labuan"
    ], key="state")
    
    phone = st.text_input("Phone Number", placeholder="e.g., 0136302897", key="phone")

    if st.button("Sign Up"):
        if validate_email(email) and validate_password(password) and password == confirm_password:
            if save_data_to_mysql(fullname, email, password, state, phone):
                st.success("Registration successful!")
                st.session_state["page"] = "LoginPage"
                st.experimental_rerun()
            else:
                st.error("Failed to register. Please try again.")
        else:
            if not validate_email(email):
                st.error("Invalid email format")
            if not validate_password(password):
                st.error("Password must be at least 8 characters long and include letters and numbers")
            if password != confirm_password:
                st.error("Passwords do not match")

    if st.button("Back to Login"):
        st.session_state["page"] = "LoginPage"
        st.experimental_rerun()

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
