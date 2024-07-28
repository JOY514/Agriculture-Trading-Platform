
import streamlit as st
import re
import mysql.connector
import base64

def validate_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_password(password):
    return re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password)

def check_credentials(email, password):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="Mirza@haziq514",
            database="agriculture"
        )
        cursor = connection.cursor()
        query = "SELECT fullname, emailaddress, password FROM atpuser WHERE BINARY emailaddress = %s AND password = %s"
        cursor.execute(query, (email, password))
        result = cursor.fetchone()
        connection.close()
        return result
    except Exception as e:
        st.error("Error while connecting to database: {}".format(e))
        return None

def main():
    image_path = "data/agri4.jpg"
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <style>
            .stApp {{
                background: url("data:image/jpg;base64,{base64_image}") no-repeat center center fixed;
                background-size: cover;
            }}
            .login-container {{
                background: rgba(0, 0, 0, 0);  /* Adjusted opacity */
                padding: 20px;
                border-radius: 10px;
                width: 100%;
                max-width: 400px;
                margin: auto;
                margin-top: 10%;
                text-align: center;
            }}
            .login-title {{
                font-size: 32px;
                margin-bottom: 20px;
                color: white;
                text-align: center;
            }}
            .stTextInput input {{
                color: white !important;
            }}
            .stTextInput input::placeholder {{
                color: white !important;
            }}
            .login-button {{
                width: 100%;
                display: flex;
                justify-content: center;
                margin-top: 10px;
            }}
            .stTextInput label {{
                color: white !important;
                font-weight: bold !important;
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

    st.markdown('<div class="header">WELCOME TO AGRICULTURE TRADING PLATFORM MALAYSIA!</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown('<div class="login-title">USER LOGIN</div>', unsafe_allow_html=True)

    email = st.text_input("Enter your email address (example: mirzanurhaziq29@gmail.com)", key="email", placeholder="Email")
    password = st.text_input("Enter your password (at least 8 characters with letters and numbers)", type="password", key="password", placeholder="Password")

    if st.button("Login", key="login"):
        if validate_email(email) and validate_password(password):
            user_details = check_credentials(email, password)
            if user_details:
                st.success("Login successful!")
                full_name = user_details[0]
                st.session_state["fullname"] = full_name
                if email == "admin@gmail.com" and password == "Admin12345":
                    st.session_state["page"] = "MANAGE DATA"
                    st.session_state["is_admin"] = True
                else:
                    st.session_state["page"] = "Home"
                    st.session_state["is_admin"] = False
                st.experimental_rerun()
            else:
                st.error("Invalid email or password")
        else:
            st.error("Invalid email or password format")

    if st.button("Forgot password?", key="forgot"):
        st.session_state["page"] = "ForgetPassword"
        st.experimental_rerun()

    if st.button("Sign up", key="signup"):
        st.session_state["page"] = "SignUp"
        st.experimental_rerun()

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
