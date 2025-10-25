import streamlit as st
import sys
from pathlib import Path
from streamlit_extras.switch_page_button import switch_page


# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.config import ADMIN_USERNAME, ADMIN_PASSWORD, DEFAULT_TUTOR_PASSWORD
from utils.database import DatabaseManager

# Page configuration
st.set_page_config(
    page_title="Login - Vocabolarium",
    page_icon="🔐",
    layout="centered"
)

# Initialize database
db = DatabaseManager()

# Custom CSS
st.markdown("""
<style>
    .login-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .login-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .login-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    .login-box {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'user_role' not in st.session_state:
    st.session_state.user_role = None

if 'user_name' not in st.session_state:
    st.session_state.user_name = None

if 'user_email' not in st.session_state:
    st.session_state.user_email = None

if st.session_state.user_role == "admin":
    switch_page("admin_dashboard")
elif st.session_state.user_role == "tutor":
    switch_page("tutor_dashboard.py")

# Header
st.markdown("""
<div class="login-header">
    <div class="login-title">🔐 VOCABOLARIUM</div>
    <div class="login-subtitle">Staff & Tutor Login Portal</div>
</div>
""", unsafe_allow_html=True)

# Login Form
with st.container():
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    
    with st.form("login_form"):
        st.markdown("### 👤 Login to Your Account")
        
        username = st.text_input(
            "Username / Email",
            placeholder="Enter your username or email",
            help="Admin: use 'admin' | Tutors: use your email address"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            help="Default tutor password: tutor123"
        )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            login_button = st.form_submit_button(
                "🚀 Login",
                use_container_width=True,
                type="primary"
            )
        
        with col2:
            back_button = st.form_submit_button(
                "← Back to Home",
                use_container_width=True
            )
    
    # Handle login
    if login_button:
        if not username or not password:
            st.error("❌ Please enter both username and password")
        else:
            # Check if admin login
            if username.lower() == ADMIN_USERNAME.lower() and password == ADMIN_PASSWORD:
                st.session_state.authenticated = True
                st.session_state.user_role = "admin"
                st.session_state.user_name = "Administrator"
                st.session_state.user_email = "admin@vocabolarium.com"
                
                st.success("✅ Admin login successful!")
                st.balloons()
                st.rerun()
            
            # Check if tutor login (email-based)
            elif "@" in username:
                tutor = db.get_tutor_by_email(username)
                
                if tutor is not None:
                    # For demo, all tutors use default password
                    # In production, implement proper password management
                    if password == DEFAULT_TUTOR_PASSWORD:
                        st.session_state.authenticated = True
                        st.session_state.user_role = "tutor"
                        st.session_state.user_name = tutor["Name"]
                        st.session_state.user_email = tutor["Email"]
                        st.session_state.tutor_id = tutor["Tutor_ID"]
                        
                        st.success(f"✅ Welcome back, {tutor['Name']}!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Invalid password")
                else:
                    st.error("❌ Tutor account not found")
            else:
                st.error("❌ Invalid credentials")
    
    if back_button:
        st.switch_page("pages/1_🏠_Home.py")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Help section
st.markdown("<br>", unsafe_allow_html=True)
st.info("""
**📌 Login Information:**

**For Administrators:**
- Username: `admin`
- Password: (configured in system)

**For Tutors:**
- Username: Your registered email address
- Default Password: `tutor123`
- First time? Contact admin for account setup

**Need Help?**
- 📧 Email: vocabolarium@gmail.com
- 📱 Phone: +63 917 123 4567
""")

# Footer
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #999; font-size: 0.9rem;">
    © 2025 Vocabolarium Language Learning Center. All rights reserved.
</div>
""", unsafe_allow_html=True)
