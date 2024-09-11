import streamlit as st
import mysql.connector
import bcrypt
import base64

# Fungsi untuk menghubungkan ke database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        port="3306",
        password="", 
        database="pertambangan"
    )

# Fungsi untuk mengambil pengguna berdasarkan username
def get_user(username):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

# Fungsi untuk memverifikasi password
def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

# Convert local image to base64
def get_base64_image(image_file):
    with open(image_file, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Halaman login
def login():
    # Set page title and icon for a welcoming feel
    st.set_page_config(page_title="Mining Dashboard F Group", page_icon="👋", layout="centered")
    
    # Hide the sidebar during login
    hide_sidebar_style = """
    <style>
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """
    st.markdown(hide_sidebar_style, unsafe_allow_html=True)

    # Load the background image and convert to base64
    img_base64 = get_base64_image("images/TG.png")

    # Set background image for login page using base64
    background_image = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(background_image, unsafe_allow_html=True)

    # Input fields without changing the default style
    st.title("Mining Dashboard F Group Corp")

    # Input fields
    username = st.text_input("Username", key="username_input")
    password = st.text_input("Password", type="password", key="password_input")
    
    if st.button("Login"):
        # Cek apakah username atau password kosong
        if not username and not password:
            st.error("Please enter both username and password.")
        elif not username:
            st.error("Please enter your username.")
        elif not password:
            st.error("Please enter your password.")
        else:
            # Jika kedua input telah diisi, lakukan pengecekan login
            user = get_user(username)
            if user and verify_password(user['password_hash'], password):
                st.success(f"Welcome, {username}!")
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.rerun()  # Refresh halaman untuk mengarahkan ke home setelah login berhasil
            else:
                st.error("Incorrect username or password.")

# Fungsi logout
def logout():
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.rerun()
