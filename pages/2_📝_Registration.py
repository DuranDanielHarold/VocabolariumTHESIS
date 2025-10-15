import streamlit as st
import sys
from pathlib import Path
import re

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.config import LANGUAGES, SESSION_INTERVALS, PAYMENT_OPTIONS
from utils.database import DatabaseManager
from utils.email_service import EmailService

# Page configuration
st.set_page_config(
    page_title="Registration - Vocabolarium",
    page_icon="📝",
    layout="centered"
)

# Initialize services
db = DatabaseManager()
email_service = EmailService()

# Custom CSS
st.markdown("""
<style>
    .registration-header {
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .registration-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .registration-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 1.5rem;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.5rem;
    }
    
    .warning-box {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 8px;
        margin: 2rem 0;
    }
    
    .warning-text {
        color: #856404;
        font-size: 0.95rem;
        font-weight: 600;
        margin: 0;
    }
    
    .success-box {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 2rem 0;
    }
    
    .error-box {
        background: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 2rem 0;
    }
    
    .info-badge {
        display: inline-block;
        background: #e7f3ff;
        color: #004085;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
    
    .tutor-card {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .tutor-card:hover {
        border-color: #667eea;
        box-shadow: 0 2px 8px rgba(102,126,234,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'registration_complete' not in st.session_state:
    st.session_state.registration_complete = False

if 'selected_language' not in st.session_state:
    st.session_state.selected_language = None

# Check if registration is already complete
if st.session_state.registration_complete:
    st.markdown("""
    <div class="success-box">
        <h2 style="color: #28a745; margin: 0;">✅ Registration Successful!</h2>
        <p style="margin-top: 1rem; font-size: 1.1rem;">
            Thank you for registering with Vocabolarium! We have sent a confirmation email 
            with payment instructions and next steps.
        </p>
        <p style="margin-top: 1rem;">
            <strong>What's Next?</strong><br>
            1. Check your email for payment instructions<br>
            2. Complete your payment using your selected method<br>
            3. Send payment receipt to our email: vocabolarium@gmail.com<br>
            4. Wait for approval (24-48 hours)<br>
            5. Receive your tutor assignment and Google Meet link<br>
            6. Start your language learning journey!
        </p>
        <hr style="margin: 1.5rem 0; border-color: rgba(0,0,0,0.1);">
        <p style="margin-top: 1rem; font-size: 0.95rem; color: #666;">
            <strong>Need Help?</strong><br>
            Contact us: vocabolarium@gmail.com | +63 917 123 4567
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state.registration_complete = False
            st.session_state.selected_language = None
            st.switch_page("pages/1_🏠_Home.py")
    with col2:
        if st.button("📝 New Registration", use_container_width=True, type="primary"):
            st.session_state.registration_complete = False
            st.session_state.selected_language = None
            st.rerun()
else:
    # Header
    st.markdown("""
    <div class="registration-header">
        <div class="registration-title">📝 VOCABOLARIUM</div>
        <div class="registration-subtitle">Language Course Registration</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Back to Home button
    if st.button("← Back to Home", key="back_to_home"):
        st.switch_page("pages/1_🏠_Home.py")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # LANGUAGE SELECTION (OUTSIDE FORM FOR DYNAMIC UPDATE)
    st.markdown('<div class="section-header">📚 Course Selection</div>', unsafe_allow_html=True)
    
    language_options = list(LANGUAGES.keys())
    default_idx = 0
    
    if st.session_state.selected_language and st.session_state.selected_language in language_options:
        default_idx = language_options.index(st.session_state.selected_language)
    
    language = st.selectbox(
        "Select Language *",
        options=language_options,
        index=default_idx,
        help="Choose the language you want to learn",
        key="language_selector"
    )
    
    # Update session state
    st.session_state.selected_language = language
    
    # Display selected language info
    if language:
        lang_info = LANGUAGES[language]
        st.markdown(f"""
        <div class="info-badge">
            💰 Price: {lang_info['price']} | 📅 {lang_info['sessions']}
        </div>
        """, unsafe_allow_html=True)
        
        # Show language description
        with st.expander("ℹ️ About this language", expanded=False):
            st.write(f"**Description:** {lang_info['description']}")
            st.write(f"**Culture:** {lang_info['culture']}")
            st.write(f"**Origin:** {lang_info['origin']}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # TUTOR SELECTION (OUTSIDE FORM FOR DYNAMIC UPDATE)
    st.markdown('<div class="section-header">👨‍🏫 Choose Your Tutor</div>', unsafe_allow_html=True)
    
    # Get tutors who teach the selected language from DATABASE
    available_tutors = db.get_tutors_by_language(language)
    
    if len(available_tutors) > 0:
        st.success(f"✅ {len(available_tutors)} expert tutor(s) available for {language}")
        
        # Display tutor options
        tutor_options = ["No Preference (Admin will assign)"] + available_tutors["Name"].tolist()
        
        selected_tutor = st.selectbox(
            "Select Your Preferred Tutor *",
            options=tutor_options,
            help="Choose your preferred tutor or let admin assign one for you",
            key="tutor_selector"
        )
        
        # Show tutor details if specific tutor is selected
        if selected_tutor != "No Preference (Admin will assign)":
            tutor_info = available_tutors[available_tutors["Name"] == selected_tutor].iloc[0]
            
            with st.expander(f"👤 About {selected_tutor}", expanded=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**📚 Specialization:** {tutor_info['Specialization']}")
                    st.write(f"**🗣️ Languages:** {tutor_info['Languages_Teaching']}")
                    st.write(f"**⭐ Rating:** {tutor_info['Rating']}/5.0")
                
                with col2:
                    st.write(f"**📅 Experience:** {tutor_info['Experience_Years']} years")
                    st.write(f"**⏰ Available:** {tutor_info['Available_Times']}")
                    st.write(f"**📞 Contact:** {tutor_info['Contact_Number']}")
                    
                # Show Tutor ID for verification
                st.caption(f"🆔 Tutor ID: {tutor_info['Tutor_ID']}")
    else:
        st.warning(f"⚠️ No tutors currently available for {language}. Admin will assign a tutor upon approval.")
        selected_tutor = "No Preference (Admin will assign)"
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Registration Form (REST OF THE FIELDS)
    with st.form("registration_form"):
        st.markdown('<div class="section-header">📋 Personal Information</div>', unsafe_allow_html=True)
        
        # Personal Information
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input(
                "Full Name *",
                placeholder="Juan Dela Cruz",
                help="Enter your complete name as it appears on official documents"
            )
        
        with col2:
            age = st.number_input(
                "Age *",
                min_value=5,
                max_value=100,
                value=25,
                help="You must be at least 5 years old to register"
            )
        
        email = st.text_input(
            "Email Address *",
            placeholder="juan.delacruz@example.com",
            help="We'll send course details and materials to this email"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-header">⏰ Schedule & Payment</div>', unsafe_allow_html=True)
        
        # Schedule
        col1, col2 = st.columns(2)
        
        with col1:
            scheduled_time = st.selectbox(
                "Preferred Time Slot *",
                options=[
                    "10:00 AM - 1:00 PM"
                ],
                help="Select your preferred class time"
            )
        
        with col2:
            session_interval = st.selectbox(
                "Sessions Per Week *",
                options=SESSION_INTERVALS,
                help="How many times per week do you want to have classes?"
            )
        
        payment_option = st.selectbox(
            "Payment Method *",
            options=PAYMENT_OPTIONS,
            help="Choose your preferred payment method"
        )
        
        # Payment instructions based on selection
        if payment_option:
            st.markdown("#### 💳 Payment Instructions")
            if payment_option == "GCash":
                st.info("""
                **GCash Payment:**
                - Number: 09069481145
                - Name: LeeAnn Librada
                - After payment, send receipt to vocabolarium@gmail.com
                """)
            elif payment_option == "Bank Transfer":
                st.info("""
                **Bank Transfer:**
                - Bank: BDO (Banco de Oro)
                - Account Name: Vocabolarium Language Center
                - Account Number: 1234567890
                - After payment, send receipt to vocabolarium@gmail.com
                """)
        
        # Important Notice
        st.markdown("""
        <div class="warning-box">
            <p class="warning-text">⚠️ IMPORTANT NOTICE</p>
            <ul style="color: #856404; margin-top: 0.5rem;">
                <li><strong>No refunds are allowed</strong> once payment is confirmed</li>
                <li>You must <strong>strictly join the Google Meet link</strong> sent to your Gmail</li>
                <li>Missing classes without prior notice may result in forfeiture</li>
                <li>Please ensure all information provided is accurate</li>
                <li>Payment must be completed within 48 hours of registration</li>
                <li>Your selected tutor preference will be honored subject to availability</li>
                <li>⚠️ IF THE SCHEDULED TIME IS NOT FULFILLED, YOU WILL BE AUTOMATICALLY CHARED 300 PESOS FOR THE SAID CLASS.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Terms and Conditions
        st.markdown("#### 📜 Terms and Conditions") 
        terms_accepted = st.checkbox(
            "I have read and agree to the terms and conditions *",
            help="You must accept the terms to proceed"
        )
        
        with st.expander("📖 Read Terms and Conditions"):
            st.markdown("""
            ### Vocabolarium Terms and Conditions
            
            **1. Registration and Payment**
            - All information provided must be accurate and truthful
            - Payment must be completed within 48 hours of registration
            - No refunds will be issued after payment confirmation
            
            **2. Tutor Assignment**
            - Tutor preferences will be honored when possible
            - Administration reserves the right to assign tutors based on availability
            - Students will be notified of tutor assignment via email
            
            **3. Class Attendance**
            - Students must join classes via the provided Google Meet link
            - Punctuality is expected; classes start at the scheduled time
            - Missed classes cannot be refunded or rescheduled without prior notice
            
            **4. Course Materials**
            - All materials are for personal use only
            - Sharing or distributing materials is strictly prohibited
            
            **5. Student Conduct**
            - Respectful behavior is expected at all times
            - Harassment or inappropriate conduct will result in immediate termination
            
            By checking the box above, you acknowledge that you have read, understood, 
            and agree to be bound by these terms and conditions.
            """)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Submit buttons
        col1, col2 = st.columns([1, 1])
        
        with col1:
            submit_button = st.form_submit_button(
                "✅ Submit Registration",
                use_container_width=True,
                type="primary"
            )
        
        with col2:
            cancel_button = st.form_submit_button(
                "❌ Cancel",
                use_container_width=True
            )
    
    # Handle form submission
    if submit_button:
        # Validation
        errors = []
        
        # Name validation
        if not full_name or len(full_name.strip()) < 3:
            errors.append("Please enter a valid full name (at least 3 characters)")
        
        # Name should contain only letters and spaces
        if full_name and not re.match(r'^[a-zA-Z\s\.]+$', full_name):
            errors.append("Name should contain only letters, spaces, and periods")
        
        # Email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        if not email or not re.match(email_pattern, email):
            errors.append("Please enter a valid email address")
        
        # Age validation
        if age < 5:
            errors.append("You must be at least 5 years old to register")
        elif age > 100:
            errors.append("Please enter a valid age")
        
        # Terms acceptance
        if not terms_accepted:
            errors.append("You must accept the terms and conditions to proceed")
        
        # Display errors or process registration
        if errors:
            st.markdown('<div class="error-box">', unsafe_allow_html=True)
            st.error("❌ Please fix the following errors:")
            for error in errors:
                st.write(f"• {error}")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Process registration
            with st.spinner("Processing your registration... Please wait."):
                # Prepare tutor name (from session state or selected value)
                preferred_tutor = "" if selected_tutor == "No Preference (Admin will assign)" else selected_tutor
                
                student_data = {
                    "name": full_name.strip(),
                    "email": email.strip().lower(),
                    "age": age,
                    "language": language,
                    "preferred_tutor": preferred_tutor,
                    "scheduled_time": scheduled_time,
                    "session_interval": session_interval,
                    "payment_option": payment_option
                }
                
                # Add to database
                success, result = db.add_student(student_data)
                
                if success:
                    # Send confirmation email
                    email_success, email_msg = email_service.send_registration_confirmation(student_data)
                    
                    if email_success:
                        st.session_state.registration_complete = True
                        st.rerun()
                    else:
                        # Registration saved but email failed
                        st.markdown(f"""
                        <div class="warning-box">
                            <p class="warning-text">⚠️ Registration Saved with Warning</p>
                            <p style="color: #856404; margin-top: 0.5rem;">
                                Your registration has been saved successfully with ID: <strong>{result}</strong>
                            </p>
                            <p style="color: #856404; margin-top: 0.5rem;">
                                However, we couldn't send the confirmation email: {email_msg}
                            </p>
                            <p style="color: #856404; margin-top: 0.5rem;">
                                <strong>Please contact us directly:</strong><br>
                                Email: vocabolarium@gmail.com<br>
                                Phone: +63 917 123 4567
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.info("💡 Your registration is saved in our system. We'll contact you shortly!")
                else:
                    st.markdown(f"""
                    <div class="error-box">
                        <p style="color: #721c24; font-weight: 600;">❌ Registration Failed</p>
                        <p style="color: #721c24; margin-top: 0.5rem;">
                            {result}
                        </p>
                        <p style="color: #721c24; margin-top: 0.5rem;">
                            Please try again or contact us at vocabolarium@gmail.com
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
    
    if cancel_button:
        st.session_state.selected_language = None
        st.switch_page("pages/1_🏠_Home.py")

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 2rem; background: #f8f9fa; border-radius: 10px; margin-top: 2rem;">
    <p style="color: #666; margin-bottom: 0.5rem;">
        <strong>Need Help?</strong>
    </p>
    <p style="color: #666; font-size: 0.9rem;">
        📧 vocabolarium@gmail.com | 📱 +63 917 123 4567<br>
        📘 facebook.com/vocabolarium | 📺 youtube.com/@vocabolarium
    </p>
    <hr style="margin: 1rem 0; border-color: rgba(0,0,0,0.1);">
    <p style="color: #999; font-size: 0.85rem; margin: 0;">
        © 2025 Vocabolarium Language Learning Center. All rights reserved.
    </p>
</div>
""", unsafe_allow_html=True)