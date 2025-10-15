import streamlit as st
import sys
from pathlib import Path
import pandas as pd

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.database import DatabaseManager
from utils.email_service import EmailService

# Page configuration
st.set_page_config(
    page_title="Admin Dashboard - Vocabolarium",
    page_icon="⚙️",
    layout="wide"
)

# Initialize services
db = DatabaseManager()
email_service = EmailService()

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("🔒 Please login to access the admin dashboard")
    if st.button("Go to Login"):
        st.switch_page("pages/3_👨‍💼_Login.py")
    st.stop()

if st.session_state.user_role != "admin":
    st.error("⛔ Access denied. Admin privileges required.")
    st.stop()

# Custom CSS
st.markdown("""
<style>
    .admin-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
    }
    
    .admin-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .stats-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        border-left: 4px solid #667eea;
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .stats-label {
        font-size: 1rem;
        color: #666;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(f"""
<div class="admin-header">
    <div class="admin-title">⚙️ Admin Dashboard</div>
    <p>Welcome back, {st.session_state.user_name}! | Manage students, tutors, and approvals</p>
</div>
""", unsafe_allow_html=True)

# Logout button
col1, col2, col3 = st.columns([3, 1, 1])
with col3:
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.session_state.user_name = None
        st.switch_page("pages/1_🏠_Home.py")

# Statistics Dashboard
students_df = db.get_all_students()
tutors_df = db.get_all_tutors()

st.subheader("📊 Overview Statistics")

stat_cols = st.columns(4)

with stat_cols[0]:
    st.markdown(f"""
    <div class="stats-card">
        <div class="stats-number">{len(students_df)}</div>
        <div class="stats-label">Total Students</div>
    </div>
    """, unsafe_allow_html=True)

with stat_cols[1]:
    pending = len(students_df[students_df['Status'] == 'Pending']) if len(students_df) > 0 else 0
    st.markdown(f"""
    <div class="stats-card" style="border-left-color: #ffc107;">
        <div class="stats-number" style="color: #ffc107;">{pending}</div>
        <div class="stats-label">Pending Approvals</div>
    </div>
    """, unsafe_allow_html=True)

with stat_cols[2]:
    approved = len(students_df[students_df['Status'] == 'Approved']) if len(students_df) > 0 else 0
    st.markdown(f"""
    <div class="stats-card" style="border-left-color: #28a745;">
        <div class="stats-number" style="color: #28a745;">{approved}</div>
        <div class="stats-label">Approved Students</div>
    </div>
    """, unsafe_allow_html=True)

with stat_cols[3]:
    st.markdown(f"""
    <div class="stats-card" style="border-left-color: #17a2b8;">
        <div class="stats-number" style="color: #17a2b8;">{len(tutors_df)}</div>
        <div class="stats-label">Active Tutors</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Tabs for different sections
tab1, tab2, tab3 = st.tabs(["👨‍🎓 Student Management", "👨‍🏫 Tutor Management", "⚙️ Settings"])

# ========== STUDENT MANAGEMENT TAB ==========
with tab1:
    st.subheader("👨‍🎓 Student Database")
    
    if len(students_df) > 0:
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.selectbox(
                "Filter by Status",
                options=["All", "Pending", "Approved", "Rejected"],
                key="status_filter"
            )
        
        with col2:
            language_filter = st.selectbox(
                "Filter by Language",
                options=["All"] + list(students_df['Language'].unique()),
                key="language_filter"
            )
        
        # Apply filters
        filtered_df = students_df.copy()
        
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df['Status'] == status_filter]
        
        if language_filter != "All":
            filtered_df = filtered_df[filtered_df['Language'] == language_filter]
        
        # Display filtered data
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Student Actions
        st.subheader("🔧 Student Actions")
        
        action_cols = st.columns([2, 2, 1])
        
        with action_cols[0]:
            selected_student = st.selectbox(
                "Select Student",
                options=students_df['Registration_ID'].tolist(),
                format_func=lambda x: f"{x} - {students_df[students_df['Registration_ID']==x]['Name'].values[0]}"
            )
        
        with action_cols[1]:
            action = st.selectbox(
                "Action",
                options=["View Details", "Approve", "Reject", "Edit", "Delete"]
            )
        
        with action_cols[2]:
            execute_action = st.button("Execute", use_container_width=True, type="primary")
        
        if execute_action and selected_student:
            student_data = students_df[students_df['Registration_ID'] == selected_student].iloc[0]
            
            if action == "View Details":
                st.markdown("### 📋 Student Details")
                detail_cols = st.columns(2)
                
                with detail_cols[0]:
                    st.write(f"**Registration ID:** {student_data['Registration_ID']}")
                    st.write(f"**Name:** {student_data['Name']}")
                    st.write(f"**Email:** {student_data['Email']}")
                    st.write(f"**Age:** {student_data['Age']}")
                    st.write(f"**Preferred Tutor:** {student_data.get('Preferred_Tutor', 'N/A')}")
                
                with detail_cols[1]:
                    st.write(f"**Language:** {student_data['Language']}")
                    st.write(f"**Scheduled Time:** {student_data['Scheduled_Time']}")
                    st.write(f"**Session Interval:** {student_data['Session_Interval']}")
                    st.write(f"**Status:** {student_data['Status']}")
                    st.write(f"**Assigned Tutor:** {student_data.get('Assigned_Tutor', 'Not assigned')}")
            
            elif action == "Approve":
                st.markdown("### ✅ Approve Student Registration")
                
                with st.form("approve_form"):
                    # Get tutors who teach this language
                    language_tutors = db.get_tutors_by_language(student_data['Language'])
                    tutor_names = language_tutors['Name'].tolist()
                    
                    # Check if student has preferred tutor
                    preferred = student_data.get('Preferred_Tutor', '')
                    default_idx = tutor_names.index(preferred) if preferred and preferred in tutor_names else 0
                    
                    if preferred:
                        st.info(f"📌 Student's preferred tutor: **{preferred}**")
                    
                    selected_tutor = st.selectbox("Assign Tutor", options=tutor_names, index=default_idx)
                    
                    google_meet_link = st.text_input(
                        "Google Meet Link",
                        value=f"https://meet.google.com/{selected_student.lower().replace('reg', '')}-vocabolarium"
                    )
                    
                    approve_button = st.form_submit_button("✅ Approve & Send Email", type="primary")
                    
                    if approve_button:
                        # Update database
                        update_data = {
                            "Status": "Approved",
                            "Assigned_Tutor": selected_tutor,
                            "Google_Meet_Link": google_meet_link
                        }
                        
                        success, msg = db.update_student(selected_student, update_data)
                        
                        if success:
                            # Send approval email
                            email_success, email_msg = email_service.send_approval_email(
                                student_data,
                                selected_tutor,
                                google_meet_link
                            )
                            
                            if email_success:
                                st.success("✅ Student approved and email sent successfully!")
                                st.balloons()
                                st.rerun()
                            else:
                                st.warning(f"Student approved but email failed: {email_msg}")
                        else:
                            st.error(f"❌ Failed to approve student: {msg}")
            
            elif action == "Reject":
                st.markdown("### ❌ Reject Student Registration")
                
                with st.form("reject_form"):
                    rejection_reason = st.text_area(
                        "Rejection Reason (Optional)",
                        placeholder="Enter reason for rejection..."
                    )
                    
                    reject_button = st.form_submit_button("❌ Confirm Rejection", type="secondary")
                    
                    if reject_button:
                        update_data = {"Status": "Rejected"}
                        success, msg = db.update_student(selected_student, update_data)
                        
                        if success:
                            # Send rejection email
                            email_service.send_rejection_email(student_data, rejection_reason)
                            st.success("✅ Student registration rejected!")
                            st.rerun()
                        else:
                            st.error(f"❌ Failed to reject: {msg}")
            
            elif action == "Edit":
                st.markdown("### ✏️ Edit Student Information")
                
                with st.form("edit_form"):
                    edit_cols = st.columns(2)
                    
                    with edit_cols[0]:
                        new_name = st.text_input("Name", value=student_data['Name'])
                        new_email = st.text_input("Email", value=student_data['Email'])
                        new_age = st.number_input("Age", value=int(student_data['Age']), min_value=5)
                    
                    with edit_cols[1]:
                        new_scheduled_time = st.text_input("Scheduled Time", value=student_data['Scheduled_Time'])
                        new_session_interval = st.text_input("Session Interval", value=student_data['Session_Interval'])
                        new_status = st.selectbox("Status", options=["Pending", "Approved", "Rejected"], 
                                                 index=["Pending", "Approved", "Rejected"].index(student_data['Status']))
                    
                    save_button = st.form_submit_button("💾 Save Changes", type="primary")
                    
                    if save_button:
                        update_data = {
                            "Name": new_name,
                            "Email": new_email,
                            "Age": new_age,
                            "Scheduled_Time": new_scheduled_time,
                            "Session_Interval": new_session_interval,
                            "Status": new_status
                        }
                        
                        success, msg = db.update_student(selected_student, update_data)
                        
                        if success:
                            st.success("✅ Student information updated successfully!")
                            st.rerun()
                        else:
                            st.error(f"❌ Failed to update: {msg}")
            
            elif action == "Delete":
                st.markdown("### 🗑️ Delete Student Record")
                st.warning("⚠️ This action cannot be undone!")
                
                confirm_delete = st.checkbox("I confirm I want to delete this student record")
                
                if confirm_delete:
                    if st.button("🗑️ Confirm Delete", type="secondary"):
                        success, msg = db.delete_student(selected_student)
                        
                        if success:
                            st.success("✅ Student record deleted successfully!")
                            st.rerun()
                        else:
                            st.error(f"❌ Failed to delete: {msg}")
    else:
        st.info("📭 No student registrations yet.")

# ========== TUTOR MANAGEMENT TAB ==========
with tab2:
    st.subheader("👨‍🏫 Tutor Database")
    
    if len(tutors_df) > 0:
        st.dataframe(
            tutors_df,
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.info("📭 No tutors in the database.")
    
    # Add New Tutor
    st.subheader("➕ Add New Tutor")
    
    with st.form("add_tutor_form"):
        tutor_cols = st.columns(2)
        
        with tutor_cols[0]:
            tutor_name = st.text_input("Tutor Name *", placeholder="Maria Santos")
            tutor_email = st.text_input("Email *", placeholder="maria@example.com")
            tutor_contact = st.text_input("Contact Number *", placeholder="+63 917 123 4567")
        
        with tutor_cols[1]:
            tutor_languages = st.multiselect(
                "Languages Teaching *",
                options=["Korean", "Japanese", "Mandarin", "English", "Filipino"]
            )
            tutor_available = st.text_input("Available Times *", placeholder="Mon-Fri 9AM-5PM")
            tutor_specialization = st.text_input("Specialization", placeholder="East Asian Languages")
        
        tutor_experience = st.number_input("Years of Experience", min_value=0, max_value=50, value=3)
        
        add_tutor_button = st.form_submit_button("➕ Add Tutor", type="primary", use_container_width=True)
        
        if add_tutor_button:
            if tutor_name and tutor_email and tutor_contact and tutor_languages and tutor_available:
                tutor_data = {
                    "name": tutor_name,
                    "email": tutor_email,
                    "languages": ", ".join(tutor_languages),
                    "available_times": tutor_available,
                    "contact": tutor_contact,
                    "specialization": tutor_specialization,
                    "experience": tutor_experience,
                    "rating": 5.0
                }
                
                success, result = db.add_tutor(tutor_data)
                
                if success:
                    st.success(f"✅ Tutor added successfully! Tutor ID: {result}")
                    st.info(f"🔐 Default login credentials:\nEmail: {tutor_email}\nPassword: tutor123")
                    st.rerun()
                else:
                    st.error(f"❌ Failed to add tutor: {result}")
            else:
                st.error("❌ Please fill in all required fields!")

# ========== SETTINGS TAB ==========
with tab3:
    st.subheader("⚙️ System Settings")
    
    # Export Data
    st.markdown("### 📥 Export Data")
    
    export_cols = st.columns(2)
    
    with export_cols[0]:
        if st.button("📊 Export Students Data", use_container_width=True):
            if len(students_df) > 0:
                csv = students_df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download Students CSV",
                    data=csv,
                    file_name="students_data.csv",
                    mime="text/csv"
                )
            else:
                st.info("No student data to export")
    
    with export_cols[1]:
        if st.button("📊 Export Tutors Data", use_container_width=True):
            if len(tutors_df) > 0:
                csv = tutors_df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download Tutors CSV",
                    data=csv,
                    file_name="tutors_data.csv",
                    mime="text/csv"
                )
            else:
                st.info("No tutor data to export")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Email Test
    st.markdown("### 📧 Test Email Service")
    
    with st.form("test_email_form"):
        test_email = st.text_input("Test Email Address", placeholder="test@example.com")
        send_test = st.form_submit_button("📧 Send Test Email", type="primary")
        
        if send_test:
            if test_email:
                with st.spinner("Sending test email..."):
                    success, msg = email_service.send_test_email(test_email)
                    
                    if success:
                        st.success(f"✅ {msg}")
                    else:
                        st.error(f"❌ {msg}")
            else:
                st.error("Please enter a valid email address")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # System Information
    st.markdown("### ℹ️ System Information")
    
    info_cols = st.columns(2)
    
    with info_cols[0]:
        st.info(f"""
        **Database Status:** ✅ Connected  
        **Students Database:** {len(students_df)} records  
        **Tutors Database:** {len(tutors_df)} records
        """)
    
    with info_cols[1]:
        st.info(f"""
        **Email Service:** Configured  
        **Admin User:** {st.session_state.user_name}  
        **System Version:** 1.1.0
        """)