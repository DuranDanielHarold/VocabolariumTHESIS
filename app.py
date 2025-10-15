import streamlit as st
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Vocabolarium - Language Learning Center",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for the landing/welcome page
st.markdown("""
<style>
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .main {
        padding: 0;
    }
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    .welcome-container {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 60vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .welcome-title {
        font-size: 4rem;
        font-weight: 900;
        color: white;
        margin-bottom: 1rem;
        text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
        animation: fadeInScale 1.2s ease-in-out;
    }
    
    .welcome-subtitle {
        font-size: 1.8rem;
        color: #f0f0f0;
        margin-bottom: 1rem;
        animation: fadeInUp 1.5s ease-in-out;
    }
    
    .welcome-description {
        font-size: 1.2rem;
        color: #e0e0e0;
        max-width: 700px;
        margin: 0 auto 2rem auto;
        line-height: 1.8;
        animation: fadeIn 2s ease-in-out;
    }
    
    @keyframes fadeInScale {
        from {
            opacity: 0;
            transform: scale(0.8);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Welcome Screen
st.markdown("""
<div class="welcome-container">
    <div class="welcome-title">🌍 VOCABOLARIUM</div>
    <div class="welcome-subtitle">Your Gateway to Global Communication</div>
    <div class="welcome-description">
        Transform your future by mastering new languages. Join thousands of learners 
        who have unlocked international opportunities through our expert-led language programs.
    </div>
</div>
""", unsafe_allow_html=True)

# Add some spacing
st.markdown("<br>", unsafe_allow_html=True)

# Feature boxes using Streamlit columns instead of HTML
st.markdown("<h2 style='text-align: center; color: #667eea; margin: 2rem 0;'>Why Choose Vocabolarium?</h2>", unsafe_allow_html=True)

# Create 4 columns for features
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: white; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); height: 100%;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>🎓</div>
        <div style='font-size: 1.3rem; font-weight: 700; color: #667eea; margin-bottom: 0.5rem;'>Expert Tutors</div>
        <div style='color: #666;'>Learn from certified native speakers</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: white; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); height: 100%;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>🌏</div>
        <div style='font-size: 1.3rem; font-weight: 700; color: #667eea; margin-bottom: 0.5rem;'>5 Languages</div>
        <div style='color: #666;'>Korean, Japanese, Mandarin, English, Filipino</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: white; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); height: 100%;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>⏰</div>
        <div style='font-size: 1.3rem; font-weight: 700; color: #667eea; margin-bottom: 0.5rem;'>Flexible Schedule</div>
        <div style='color: #666;'>Choose times that work for you</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background: white; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); height: 100%;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>💻</div>
        <div style='font-size: 1.3rem; font-weight: 700; color: #667eea; margin-bottom: 0.5rem;'>Online Classes</div>
        <div style='color: #666;'>Learn from anywhere via Google Meet</div>
    </div>
    """, unsafe_allow_html=True)

# Add spacing
st.markdown("<br><br>", unsafe_allow_html=True)

# Call to Action - Centered buttons
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # Main CTA button
    if st.button("🚀 START LEARNING TODAY", use_container_width=True, type="primary", key="start_learning"):
        st.switch_page("pages/1_🏠_Home.py")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Secondary buttons
    admin_col1, admin_col2 = st.columns(2)
    
    with admin_col1:
        if st.button("👨‍💼 Staff Login", use_container_width=True, key="admin_login"):
            st.switch_page("pages/3_👨‍💼_Login.py")
    
    with admin_col2:
        if st.button("📝 Quick Register", use_container_width=True, key="quick_register"):
            st.switch_page("pages/2_📝_Registration.py")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 2rem; background: #f8f9fa; border-top: 1px solid #e0e0e0;">
    <p style="font-size: 1.1rem; color: #667eea; font-weight: 600; margin-bottom: 1rem;">
        📞 Contact Us
    </p>
    <p style="color: #666; margin-bottom: 0.5rem;">
        📧 vocabolarium@gmail.com | 📱 +63 917 123 4567
    </p>
    <p style="color: #999; font-size: 0.9rem; margin-top: 1rem;">
        © 2025 Vocabolarium Language Learning Center. All rights reserved.
    </p>
</div>
""", unsafe_allow_html=True)