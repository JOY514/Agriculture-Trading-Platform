
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

# Function to update password in the database
def update_password(email, new_password):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="Mirza@haziq514",
            database="agriculture"
        )
        cursor = connection.cursor()

        # Update password query
        update_query = """
        UPDATE atpuser
        SET password = %s
        WHERE emailaddress = %s
        """
        cursor.execute(update_query, (new_password, email))
        connection.commit()
        cursor.close()
        connection.close()
        return True
    except Exception as e:
        print("Error while updating password:", e)
        return False

# Function to check if email exists in the database
def email_exists_in_database(email):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            port="3306",
            user="root",
            password="Mirza@haziq514",
            database="agriculture"
        )
        cursor = connection.cursor()

        # Check email existence query
        select_query = """
        SELECT COUNT(*) FROM atpuser WHERE emailaddress = %s
        """
        cursor.execute(select_query, (email,))
        result = cursor.fetchone()
        cursor.close()
        connection.close()

        # If count is greater than 0, email exists in the database
        return result[0] > 0
    except Exception as e:
        print("Error while checking email existence:", e)
        return False

def main():
    image_path = "data/agri2.jpg"
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <style>
            .stApp {{
                background: url("data:image/jpg;base64,{base64_image}") no-repeat center center fixed;
                background-size: cover;
            }}
            .forgot-container {{
                background: rgba(0, 0, 0, 0);  /* Adjusted opacity */
                padding: 20px;
                border-radius: 10px;
                width: 100%;
                max-width: 400px;
                margin: auto;
                margin-top: 10%;
                text-align: center;
            }}
            .forgot-title {{
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
            .forgot-button {{
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

    st.markdown('<div class="header">DONT WORRY OUR TEAM WILL HELP YOU!</div>', unsafe_allow_html=True)
    st.markdown('<div class="forgot-container">', unsafe_allow_html=True)
    st.markdown('<div class="forgot-title">Forget Password</div>', unsafe_allow_html=True)

    # User input for email address
    email = st.text_input("Enter your email address")

    # Prompt user to enter new password and confirm password
    new_password = st.text_input("New Password", type="password", placeholder="e.g., Abc12345")
    confirm_password = st.text_input("Confirm New Password", type="password")
    if new_password != "" and confirm_password != "":
        if new_password == confirm_password:
            # Validate the new password format
            if validate_password(new_password):
                # Update password in the database
                if update_password(email, new_password):
                    st.success("Password updated successfully!")
                    if st.button("Back to Login"):
                        st.session_state["page"] = "LoginPage"
                        st.experimental_rerun()
                else:
                    st.error("Failed to update password.")
            else:
                st.error("Password must be at least 8 characters long and include letters and numbers.")
        else:
            st.error("Passwords do not match.")
    
    # Check if email exists in the database
    if validate_email(email):
        if email_exists_in_database(email):
            st.success("Email address found in the database")
        else:
            st.error("Email address not found in the database.")
    else:
        st.error("Invalid email address")

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
