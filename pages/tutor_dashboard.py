import streamlit as st
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.database import DatabaseManager

# Page configuration
st.set_page_config(
    page_title="Tutor Dashboard - Vocabolarium",
    page_icon="👨‍🏫",
    layout="wide"
)

# Initialize database
db = DatabaseManager()

# Check authentication
if 'authenticated' not in st.session_state or not st.session_state.authenticated:
    st.error("🔒 Please login to access the tutor dashboard")
    if st.button("Go to Login"):
        st.switch_page("pages/3_👨‍💼_Login.py")
    st.stop()

if st.session_state.user_role != "tutor":
    st.error("⛔ Access denied. Tutor privileges required.")
    st.stop()

# Custom CSS
st.markdown("""
<style>
    .tutor-header {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
    }
    
    .tutor-title {
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
        border-left: 4px solid #11998e;
    }
    
    .stats-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #11998e;
    }
    
    .stats-label {
        font-size: 1rem;
        color: #666;
        margin-top: 0.5rem;
    }
    
    .student-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    
    .student-name {
        font-size: 1.3rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Get tutor information
tutor_name = st.session_state.user_name
tutor_email = st.session_state.user_email
tutor_info = db.get_tutor_by_email(tutor_email)

# Header
st.markdown(f"""
<div class="tutor-header">
    <div class="tutor-title">👨‍🏫 Tutor Dashboard</div>
    <p>Welcome, {tutor_name}! | Monitor your students and manage your classes</p>
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

# Get students assigned to this tutor
my_students = db.get_students_by_tutor(tutor_name)

# Statistics Dashboard
st.subheader("📊 My Statistics")

stat_cols = st.columns(4)

with stat_cols[0]:
    st.markdown(f"""
    <div class="stats-card">
        <div class="stats-number">{len(my_students)}</div>
        <div class="stats-label">Total Students</div>
    </div>
    """, unsafe_allow_html=True)

with stat_cols[1]:
    active_students = len(my_students[my_students['Status'] == 'Approved']) if len(my_students) > 0 else 0
    st.markdown(f"""
    <div class="stats-card" style="border-left-color: #28a745;">
        <div class="stats-number" style="color: #28a745;">{active_students}</div>
        <div class="stats-label">Active Students</div>
    </div>
    """, unsafe_allow_html=True)

with stat_cols[2]:
    languages_teaching = tutor_info['Languages_Teaching'].split(", ") if tutor_info is not None else []
    st.markdown(f"""
    <div class="stats-card" style="border-left-color: #667eea;">
        <div class="stats-number" style="color: #667eea;">{len(languages_teaching)}</div>
        <div class="stats-label">Languages Teaching</div>
    </div>
    """, unsafe_allow_html=True)

with stat_cols[3]:
    rating = tutor_info['Rating'] if tutor_info is not None else 0
    st.markdown(f"""
    <div class="stats-card" style="border-left-color: #ffc107;">
        <div class="stats-number" style="color: #ffc107;">{rating}</div>
        <div class="stats-label">My Rating</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3 = st.tabs(["👥 My Students", "📅 Schedule Overview", "👤 My Profile"])

# ========== MY STUDENTS TAB ==========
with tab1:
    st.subheader("👥 My Students")
    
    if len(my_students) > 0:
        # Filter by status
        status_filter = st.selectbox(
            "Filter by Status",
            options=["All", "Pending", "Approved", "Active", "Completed"],
            key="student_status_filter"
        )
        
        filtered_students = my_students.copy()
        if status_filter != "All":
            filtered_students = filtered_students[filtered_students['Status'] == status_filter]
        
        st.markdown(f"**Showing {len(filtered_students)} student(s)**")
        
        # Display students as cards
        for idx, student in filtered_students.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="student-card">
                    <div class="student-name">📚 {student['Name']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**📧 Email:** {student['Email']}")
                    st.write(f"**🎂 Age:** {student['Age']}")
                    st.write(f"**🌍 Language:** {student['Language']}")
                
                with col2:
                    st.write(f"**⏰ Class Time:** {student['Scheduled_Time']}")
                    st.write(f"**📅 Frequency:** {student['Session_Interval']}")
                    st.write(f"**💳 Payment:** {student['Payment_Option']}")
                
                with col3:
                    st.write(f"**📋 Status:** {student['Status']}")
                    st.write(f"**📅 Registered:** {student['Registration_Date']}")
                    
                    # Google Meet Link
                    if student['Google_Meet_Link']:
                        st.markdown(f"**📹 [Join Google Meet]({student['Google_Meet_Link']})**")
                    else:
                        st.write("**📹 Meet Link:** Not assigned yet")
                
                # Add notes section
                with st.expander(f"📝 Notes for {student['Name']}"):
                    current_notes = student.get('Notes', '')
                    
                    with st.form(f"notes_form_{student['Registration_ID']}"):
                        new_notes = st.text_area(
                            "Student Notes",
                            value=current_notes,
                            placeholder="Add notes about this student's progress, behavior, attendance, etc.",
                            height=100
                        )
                        
                        if st.form_submit_button("💾 Save Notes"):
                            update_data = {"Notes": new_notes}
                            success, msg = db.update_student(student['Registration_ID'], update_data)
                            
                            if success:
                                st.success("✅ Notes saved successfully!")
                                st.rerun()
                            else:
                                st.error(f"❌ Failed to save notes: {msg}")
                
                st.markdown("<hr>", unsafe_allow_html=True)
        
        # Summary table
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📊 Student Summary Table")
        
        summary_df = filtered_students[[
            'Registration_ID', 'Name', 'Email', 'Language', 
            'Scheduled_Time', 'Session_Interval', 'Status'
        ]].copy()
        
        st.dataframe(summary_df, use_container_width=True, hide_index=True)
        
    else:
        st.info("📭 No students assigned to you yet. Check back later!")

# ========== SCHEDULE OVERVIEW TAB ==========
with tab2:
    st.subheader("📅 My Class Schedule")
    
    if len(my_students) > 0:
        # Group by time slot
        schedule_df = my_students[my_students['Status'].isin(['Approved', 'Active'])].copy()
        
        if len(schedule_df) > 0:
            # Sort by scheduled time
            schedule_df = schedule_df.sort_values('Scheduled_Time')
            
            # Display schedule by day
            st.markdown("### 🗓️ Weekly Schedule")
            
            # Create a visual schedule
            for time_slot in schedule_df['Scheduled_Time'].unique():
                students_at_time = schedule_df[schedule_df['Scheduled_Time'] == time_slot]
                
                st.markdown(f"#### ⏰ {time_slot}")
                
                for idx, student in students_at_time.iterrows():
                    col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
                    
                    with col1:
                        st.write(f"**👤 {student['Name']}**")
                    
                    with col2:
                        st.write(f"📚 {student['Language']}")
                    
                    with col3:
                        st.write(f"📅 {student['Session_Interval']}")
                    
                    with col4:
                        if student['Google_Meet_Link']:
                            st.markdown(f"[📹 Join Class]({student['Google_Meet_Link']})")
                        else:
                            st.write("No link yet")
                
                st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)
            
            # Download schedule
            st.markdown("<br>", unsafe_allow_html=True)
            csv = schedule_df[['Name', 'Language', 'Scheduled_Time', 'Session_Interval', 'Email']].to_csv(index=False)
            st.download_button(
                label="📥 Download My Schedule",
                data=csv,
                file_name=f"schedule_{tutor_name.replace(' ', '_')}.csv",
                mime="text/csv"
            )
        else:
            st.info("📭 No active classes scheduled yet.")
    else:
        st.info("📭 No students assigned to you yet.")

# ========== MY PROFILE TAB ==========
with tab3:
    st.subheader("👤 My Profile")
    
    if tutor_info is not None:
        # Display profile information
        profile_cols = st.columns([1, 2])
        
        with profile_cols[0]:
            st.markdown("""
            <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); border-radius: 15px; color: white;">
                <div style="font-size: 4rem;">👨‍🏫</div>
                <div style="font-size: 1.5rem; font-weight: 700; margin-top: 1rem;">""" + tutor_name + """</div>
                <div style="font-size: 1rem; opacity: 0.9; margin-top: 0.5rem;">""" + tutor_info['Specialization'] + """</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Rating display
            rating = tutor_info['Rating']
            stars = "⭐" * int(rating)
            st.markdown(f"### {stars} {rating}/5.0")
        
        with profile_cols[1]:
            st.markdown("### 📋 Profile Information")
            
            info_container = st.container()
            
            with info_container:
                st.write(f"**🆔 Tutor ID:** {tutor_info['Tutor_ID']}")
                st.write(f"**👤 Full Name:** {tutor_info['Name']}")
                st.write(f"**📧 Email:** {tutor_info['Email']}")
                st.write(f"**📞 Contact:** {tutor_info['Contact_Number']}")
                st.write(f"**🗣️ Languages Teaching:** {tutor_info['Languages_Teaching']}")
                st.write(f"**⏰ Available Times:** {tutor_info['Available_Times']}")
                st.write(f"**📚 Specialization:** {tutor_info['Specialization']}")
                st.write(f"**📅 Experience:** {tutor_info['Experience_Years']} years")
                st.write(f"**✅ Status:** {tutor_info['Status']}")
                st.write(f"**📆 Date Added:** {tutor_info['Date_Added']}")
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Update profile section
        st.markdown("### ✏️ Update Profile")
        
        with st.form("update_profile_form"):
            update_cols = st.columns(2)
            
            with update_cols[0]:
                new_contact = st.text_input("Contact Number", value=tutor_info['Contact_Number'])
                new_available = st.text_input("Available Times", value=tutor_info['Available_Times'])
            
            with update_cols[1]:
                new_specialization = st.text_input("Specialization", value=tutor_info['Specialization'])
                new_languages = st.multiselect(
                    "Languages Teaching",
                    options=["Korean", "Japanese", "Mandarin", "English", "Filipino"],
                    default=tutor_info['Languages_Teaching'].split(", ")
                )
            
            if st.form_submit_button("💾 Update Profile", type="primary"):
                update_data = {
                    "Contact_Number": new_contact,
                    "Available_Times": new_available,
                    "Specialization": new_specialization,
                    "Languages_Teaching": ", ".join(new_languages)
                }
                
                success, msg = db.update_tutor(tutor_info['Tutor_ID'], update_data)
                
                if success:
                    st.success("✅ Profile updated successfully!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"❌ Failed to update profile: {msg}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Change password section (placeholder for future implementation)
        st.markdown("### 🔐 Change Password")
        st.info("🔧 Password change feature coming soon. Contact admin to change your password.")
        
    else:
        st.error("❌ Could not load tutor profile information.")

# Footer with quick stats
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

footer_cols = st.columns(4)

with footer_cols[0]:
    st.metric("Total Students", len(my_students))

with footer_cols[1]:
    active = len(my_students[my_students['Status'] == 'Approved']) if len(my_students) > 0 else 0
    st.metric("Active Classes", active)

with footer_cols[2]:
    languages = len(tutor_info['Languages_Teaching'].split(", ")) if tutor_info is not None else 0
    st.metric("Languages", languages)

with footer_cols[3]:
    experience = tutor_info['Experience_Years'] if tutor_info is not None else 0
    st.metric("Experience", f"{experience} years")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; padding: 1rem; color: #999; font-size: 0.9rem;">
    © 2025 Vocabolarium Language Learning Center. All rights reserved.
</div>
""", unsafe_allow_html=True)
