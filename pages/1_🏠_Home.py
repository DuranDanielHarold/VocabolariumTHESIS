import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.config import LANGUAGES, CONTACT_INFO

# Page configuration
st.set_page_config(
    page_title="Vocabolarium - Language Learning Center",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for animations and styling
st.markdown("""
<style>
    /* Global Styles */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Header Styles */
    .header-container {
        text-align: center;
        padding: 3rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        margin-bottom: 3rem;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    
    .main-title {
        font-size: 4rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        animation: fadeInDown 1s ease-in-out;
    }
    
    .subtitle {
        font-size: 1.5rem;
        color: #f0f0f0;
        margin-bottom: 1rem;
        animation: fadeInUp 1s ease-in-out;
    }
    
    .description {
        font-size: 1.1rem;
        color: #e0e0e0;
        max-width: 800px;
        margin: 0 auto;
        line-height: 1.6;
        animation: fadeIn 1.5s ease-in-out;
    }
    
    /* Language Card Styles */
    .language-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        height: 100%;
        border: 2px solid transparent;
        cursor: pointer;
    }
    
    .language-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.15);
        border-color: #667eea;
    }
    
    .language-title {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .language-description {
        font-size: 0.95rem;
        color: #555;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    .language-info {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
    
    .price-tag {
        font-size: 1.5rem;
        font-weight: 700;
        color: #28a745;
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Feature Cards */
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .feature-card:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .feature-description {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* Testimonial Section */
    .testimonial-section {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        color: white;
        margin: 3rem 0;
    }
    
    .testimonial-text {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    /* Footer */
    .footer {
        background: #2c3e50;
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 3rem;
    }
    
    .footer-title {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
    }
    
    .footer-content {
        display: flex;
        justify-content: space-around;
        flex-wrap: wrap;
    }
    
    .footer-section {
        margin: 1rem;
    }
    
    .footer-link {
        color: #3498db;
        text-decoration: none;
        font-size: 1.1rem;
    }
    
    .footer-link:hover {
        color: #5dade2;
        text-decoration: underline;
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
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
    
    /* Section Titles */
    .section-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin: 3rem 0 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header Section
st.markdown("""
<div class="header-container">
    <div class="main-title">🌍 VOCABOLARIUM</div>
    <div class="subtitle">Unlock Your Global Potential</div>
    <div class="description">
        Master new languages with expert tutors, flexible scheduling, and immersive learning experiences. 
        Your journey to becoming multilingual starts here!
    </div>
</div>
""", unsafe_allow_html=True)

# Languages Section
st.markdown('<div class="section-title">🗣️ Our Language Programs</div>', unsafe_allow_html=True)

# Create columns for language cards
cols = st.columns(3)
language_list = list(LANGUAGES.keys())

for idx, lang_name in enumerate(language_list):
    col_idx = idx % 3
    with cols[col_idx]:
        lang_info = LANGUAGES[lang_name]
        
        # Create expandable card
        with st.expander(f"🌟 {lang_name}", expanded=False):
            st.markdown(f"""
            <div class="language-description">
                <strong>📖 About:</strong><br>
                {lang_info['description']}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="language-description">
                <strong>🎭 Culture:</strong><br>
                {lang_info['culture']}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="language-description">
                <strong>📜 Origin:</strong><br>
                {lang_info['origin']}
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f'<div class="price-tag">💰 {lang_info["price"]}</div>', unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center; color: #555;'>📅 {lang_info['sessions']}</p>", unsafe_allow_html=True)
            
            # Inquire button
            if st.button(f"📝 Inquire Now - {lang_name}", key=f"inquire_{lang_name}", use_container_width=True):
                st.session_state.selected_language = lang_name
                st.switch_page("pages/2_📝_Registration.py")

# Features Section
st.markdown('<div class="section-title">✨ Why Choose Vocabolarium?</div>', unsafe_allow_html=True)

feature_cols = st.columns(3)

features = [
    {
        "icon": "⚡",
        "title": "Quick Learning",
        "description": "Our proven methodology helps you achieve fluency faster with interactive sessions and practical exercises."
    },
    {
        "icon": "💳",
        "title": "Easy Payment",
        "description": "Multiple payment options including GCash, Bank Transfer, and PayPal. Simple, secure, and convenient."
    },
    {
        "icon": "🕐",
        "title": "Time Flexible",
        "description": "Choose your preferred schedule with sessions from 2-5 times per week. Learn at your own pace!"
    }
]

for idx, feature in enumerate(features):
    with feature_cols[idx]:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">{feature['icon']}</div>
            <div class="feature-title">{feature['title']}</div>
            <div class="feature-description">{feature['description']}</div>
        </div>
        """, unsafe_allow_html=True)

# Testimonial/CTA Section
st.markdown("""
<div class="testimonial-section">
    <div class="testimonial-text">🎯 Be The First To Testimony!</div>
    <p style="font-size: 1.2rem; opacity: 0.95;">
        Join hundreds of successful language learners who have transformed their lives through Vocabolarium. 
        Your success story starts today!
    </p>
</div>
""", unsafe_allow_html=True)

# Additional Info Section
st.markdown('<div class="section-title">📚 What You\'ll Get</div>', unsafe_allow_html=True)

info_cols = st.columns(2)

with info_cols[0]:
    st.markdown("""
    ### 🎓 Comprehensive Learning Materials
    - Professional PDF modules for each language
    - Interactive exercises and assignments
    - Cultural insights and real-world applications
    - Progress tracking and assessments
    """)
    
    st.markdown("""
    ### 👨‍🏫 Expert Tutors
    - Native or near-native speakers
    - Certified language instructors
    - Personalized learning approach
    - One-on-one attention
    """)

with info_cols[1]:
    st.markdown("""
    ### 💻 Modern Learning Platform
    - Virtual classes via Google Meet
    - Flexible scheduling options
    - Record sessions for review
    - Interactive digital tools
    """)
    
    st.markdown("""
    ### 🎯 Results-Oriented
    - Structured curriculum
    - Regular progress evaluations
    - Certificate upon completion
    - Guaranteed improvement
    """)

# Call to Action
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 START YOUR JOURNEY NOW", use_container_width=True, type="primary"):
        st.switch_page("pages/2_📝_Registration.py")

# Footer Section
st.markdown("""
<div class="footer">
    <div class="footer-title">📞 Contact Us</div>
    <div class="footer-content">
        <div class="footer-section">
            <strong>📧 Email:</strong><br>
            <a href="mailto:vocabolarium@gmail.com" class="footer-link">vocabolarium@gmail.com</a>
        </div>
        <div class="footer-section">
            <strong>📱 Phone:</strong><br>
            <span style="color: white;">+63 917 123 4567</span>
        </div>
        <div class="footer-section">
            <strong>📘 Facebook:</strong><br>
            <a href="https://facebook.com/vocabolarium" target="_blank" class="footer-link">@vocabolarium</a>
        </div>
        <div class="footer-section">
            <strong>📺 YouTube:</strong><br>
            <a href="https://youtube.com/@vocabolarium" target="_blank" class="footer-link">@vocabolarium</a>
        </div>
    </div>
    <hr style="margin: 2rem 0; border-color: rgba(255,255,255,0.2);">
    <p style="text-align: center; opacity: 0.8;">
        © 2025 Vocabolarium Language Learning Center. All rights reserved.<br>
        <em>"Connecting Cultures Through Language"</em>
    </p>
</div>
""", unsafe_allow_html=True)