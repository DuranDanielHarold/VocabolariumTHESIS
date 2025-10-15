"""
Database Manager for Vocabolarium
Handles all database operations for students and tutors using Excel files
Provides CRUD operations with error handling and data validation
"""

import pandas as pd
import os
from datetime import datetime
from pathlib import Path
import sys
from typing import Dict, Tuple, List, Optional
import logging

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.config import STUDENTS_DB, TUTORS_DB, DATA_DIR

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Comprehensive database manager for Excel-based storage
    Handles students and tutors data with full CRUD operations
    """
    
    def __init__(self):
        """Initialize database manager and create databases if needed"""
        # Ensure data directory exists
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        self._initialize_databases()
        logger.info("DatabaseManager initialized successfully")
    
    def _initialize_databases(self):
        """Initialize Excel databases if they don't exist"""
        self._initialize_students_db()
        self._initialize_tutors_db()
    
    def _initialize_students_db(self):
        """Initialize Students Database"""
        if not STUDENTS_DB.exists():
            logger.info("Creating new students database...")
            students_df = pd.DataFrame(columns=[
                "Registration_ID",
                "Name",
                "Email",
                "Age",
                "Language",
                "Preferred_Tutor",
                "Scheduled_Time",
                "Session_Interval",
                "Payment_Option",
                "Registration_Date",
                "Status",
                "Assigned_Tutor",
                "Google_Meet_Link",
                "Payment_Status",
                "Payment_Date",
                "Notes"
            ])
            students_df.to_excel(STUDENTS_DB, index=False, engine='openpyxl')
            logger.info(f"Students database created at {STUDENTS_DB}")
        else:
            # Check if Preferred_Tutor column exists, add if not
            try:
                df = pd.read_excel(STUDENTS_DB, engine='openpyxl')
                if "Preferred_Tutor" not in df.columns:
                    df["Preferred_Tutor"] = ""
                    df.to_excel(STUDENTS_DB, index=False, engine='openpyxl')
                    logger.info("Added Preferred_Tutor column to students database")
            except:
                pass
            logger.info(f"Students database found at {STUDENTS_DB}")
    
    def _initialize_tutors_db(self):
        """Initialize Tutors Database with sample data"""
        if not TUTORS_DB.exists():
            logger.info("Creating new tutors database...")
            tutors_df = pd.DataFrame(columns=[
                "Tutor_ID",
                "Name",
                "Email",
                "Languages_Teaching",
                "Available_Times",
                "Contact_Number",
                "Date_Added",
                "Status",
                "Specialization",
                "Experience_Years",
                "Rating"
            ])
            
            # Add sample tutors
            sample_tutors = [
                {
                    "Tutor_ID": "TUT001",
                    "Name": "Angeline Janer",
                    "Email": "maria.santos@vocabolarium.com",
                    "Languages_Teaching": "Korean, Japanese",
                    "Available_Times": "Mon-Fri 9AM-5PM",
                    "Contact_Number": "+63 917 111 2222",
                    "Date_Added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Status": "Active",
                    "Specialization": "East Asian Languages",
                    "Experience_Years": 5,
                    "Rating": 4.8
                },
                {
                    "Tutor_ID": "TUT002",
                    "Name": "Ashanti Jumawan",
                    "Email": "john.chen@vocabolarium.com",
                    "Languages_Teaching": "Mandarin, English",
                    "Available_Times": "Mon-Fri 1PM-9PM",
                    "Contact_Number": "+63 917 333 4444",
                    "Date_Added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Status": "Active",
                    "Specialization": "Business Languages",
                    "Experience_Years": 8,
                    "Rating": 4.9
                },
                {
                    "Tutor_ID": "TUT003",
                    "Name": "LeeAnn Librada",
                    "Email": "ana.reyes@vocabolarium.com",
                    "Languages_Teaching": "Filipino, English, Mandarin, Korean, Japanese",
                    "Available_Times": "Mon-Sat 8AM-4PM",
                    "Contact_Number": "+63 917 555 6666",
                    "Date_Added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Status": "Active",
                    "Specialization": "Flexibility Languages",
                    "Experience_Years": 3,
                    "Rating": 4.7
                },
                {
                    "Tutor_ID": "TUT004",
                    "Name": "Mariella Joy Marquez",
                    "Email": "kim.minjun@vocabolarium.com",
                    "Languages_Teaching": "Korean",
                    "Available_Times": "Tue-Sat 10AM-6PM",
                    "Contact_Number": "+63 917 777 8888",
                    "Date_Added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Status": "Active",
                    "Specialization": "Korean Culture & Language",
                    "Experience_Years": 6,
                    "Rating": 4.9
                },
                {
                    "Tutor_ID": "TUT005",
                    "Name": "Princess Erica Ingco",
                    "Email": "sakura.tanaka@vocabolarium.com",
                    "Languages_Teaching": "Japanese",
                    "Available_Times": "Mon-Fri 2PM-8PM",
                    "Contact_Number": "+63 917 999 0000",
                    "Date_Added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Status": "Active",
                    "Specialization": "Japanese Language & Literature",
                    "Experience_Years": 7,
                    "Rating": 5.0
                },

            ]
            
            tutors_df = pd.DataFrame(sample_tutors)
            tutors_df.to_excel(TUTORS_DB, index=False, engine='openpyxl')
            logger.info(f"Tutors database created with {len(sample_tutors)} sample tutors at {TUTORS_DB}")
        else:
            logger.info(f"Tutors database found at {TUTORS_DB}")
    
    # ==================== STUDENT OPERATIONS ====================
    
    def add_student(self, student_data: Dict) -> Tuple[bool, str]:
        """
        Add new student to database
        
        Args:
            student_data: Dictionary containing student information
            
        Returns:
            Tuple of (success: bool, message/registration_id: str)
        """
        try:
            df = pd.read_excel(STUDENTS_DB, engine='openpyxl')
            
            # Generate Registration ID
            if len(df) > 0 and 'Registration_ID' in df.columns:
                last_id = df["Registration_ID"].max()
                if pd.notna(last_id):
                    new_id_num = int(last_id.replace('REG', '')) + 1
                    new_id = f"REG{new_id_num:04d}"
                else:
                    new_id = "REG0001"
            else:
                new_id = "REG0001"
            
            # Prepare student record
            new_student = {
                "Registration_ID": new_id,
                "Name": student_data.get("name", ""),
                "Email": student_data.get("email", "").lower(),
                "Age": student_data.get("age", 0),
                "Language": student_data.get("language", ""),
                "Preferred_Tutor": student_data.get("preferred_tutor", ""),
                "Scheduled_Time": student_data.get("scheduled_time", ""),
                "Session_Interval": student_data.get("session_interval", ""),
                "Payment_Option": student_data.get("payment_option", ""),
                "Registration_Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Status": "Pending",
                "Assigned_Tutor": student_data.get("preferred_tutor", ""),
                "Google_Meet_Link": "",
                "Payment_Status": "Pending",
                "Payment_Date": "",
                "Notes": ""
            }
            
            # Append to dataframe
            df = pd.concat([df, pd.DataFrame([new_student])], ignore_index=True)
            df.to_excel(STUDENTS_DB, index=False, engine='openpyxl')
            
            logger.info(f"Student added successfully: {new_id}")
            return True, new_id
            
        except Exception as e:
            logger.error(f"Error adding student: {str(e)}")
            return False, str(e)
    
    def get_all_students(self) -> pd.DataFrame:
        """
        Get all students from database
        
        Returns:
            DataFrame containing all students
        """
        try:
            df = pd.read_excel(STUDENTS_DB, engine='openpyxl')
            logger.info(f"Retrieved {len(df)} students from database")
            return df
        except Exception as e:
            logger.error(f"Error reading students database: {str(e)}")
            return pd.DataFrame()
    
    def get_student_by_id(self, registration_id: str) -> Optional[pd.Series]:
        """
        Get student by registration ID
        
        Args:
            registration_id: Student's registration ID
            
        Returns:
            Series containing student data or None
        """
        try:
            df = pd.read_excel(STUDENTS_DB, engine='openpyxl')
            student = df[df["Registration_ID"] == registration_id]
            
            if len(student) > 0:
                return student.iloc[0]
            return None
            
        except Exception as e:
            logger.error(f"Error getting student {registration_id}: {str(e)}")
            return None
    
    def get_students_by_status(self, status: str) -> pd.DataFrame:
        """
        Get students filtered by status
        
        Args:
            status: Status to filter by (Pending, Approved, Rejected)
            
        Returns:
            DataFrame containing filtered students
        """
        try:
            df = pd.read_excel(STUDENTS_DB, engine='openpyxl')
            filtered = df[df["Status"] == status]
            logger.info(f"Retrieved {len(filtered)} students with status '{status}'")
            return filtered
        except Exception as e:
            logger.error(f"Error filtering students by status: {str(e)}")
            return pd.DataFrame()
    
    def get_students_by_language(self, language: str) -> pd.DataFrame:
        """
        Get students filtered by language
        
        Args:
            language: Language to filter by
            
        Returns:
            DataFrame containing filtered students
        """
        try:
            df = pd.read_excel(STUDENTS_DB, engine='openpyxl')
            filtered = df[df["Language"] == language]
            logger.info(f"Retrieved {len(filtered)} students learning '{language}'")
            return filtered
        except Exception as e:
            logger.error(f"Error filtering students by language: {str(e)}")
            return pd.DataFrame()
    
    def get_students_by_tutor(self, tutor_name: str) -> pd.DataFrame:
        """
        Get all students assigned to a specific tutor
        
        Args:
            tutor_name: Name of the tutor
            
        Returns:
            DataFrame containing students assigned to this tutor
        """
        try:
            df = pd.read_excel(STUDENTS_DB, engine='openpyxl')
            filtered = df[df["Assigned_Tutor"] == tutor_name]
            logger.info(f"Retrieved {len(filtered)} students for tutor '{tutor_name}'")
            return filtered
        except Exception as e:
            logger.error(f"Error filtering students by tutor: {str(e)}")
            return pd.DataFrame()
    
    def update_student(self, registration_id: str, update_data: Dict) -> Tuple[bool, str]:
        """
        Update student record
        
        Args:
            registration_id: Student's registration ID
            update_data: Dictionary with fields to update
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            df = pd.read_excel(STUDENTS_DB, engine='openpyxl')
            idx = df[df["Registration_ID"] == registration_id].index
            
            if len(idx) > 0:
                for key, value in update_data.items():
                    if key in df.columns:
                        df.loc[idx[0], key] = value
                
                df.to_excel(STUDENTS_DB, index=False, engine='openpyxl')
                logger.info(f"Student {registration_id} updated successfully")
                return True, "Student updated successfully"
            else:
                logger.warning(f"Student {registration_id} not found")
                return False, "Student not found"
                
        except Exception as e:
            logger.error(f"Error updating student {registration_id}: {str(e)}")
            return False, str(e)
    
    def delete_student(self, registration_id: str) -> Tuple[bool, str]:
        """
        Delete student record
        
        Args:
            registration_id: Student's registration ID
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            df = pd.read_excel(STUDENTS_DB, engine='openpyxl')
            initial_len = len(df)
            
            df = df[df["Registration_ID"] != registration_id]
            
            if len(df) < initial_len:
                df.to_excel(STUDENTS_DB, index=False, engine='openpyxl')
                logger.info(f"Student {registration_id} deleted successfully")
                return True, "Student deleted successfully"
            else:
                logger.warning(f"Student {registration_id} not found for deletion")
                return False, "Student not found"
                
        except Exception as e:
            logger.error(f"Error deleting student {registration_id}: {str(e)}")
            return False, str(e)
    
    def search_students(self, search_term: str) -> pd.DataFrame:
        """
        Search students by name or email
        
        Args:
            search_term: Term to search for
            
        Returns:
            DataFrame containing matching students
        """
        try:
            df = pd.read_excel(STUDENTS_DB, engine='openpyxl')
            search_term = search_term.lower()
            
            mask = (
                df["Name"].str.lower().str.contains(search_term, na=False) |
                df["Email"].str.lower().str.contains(search_term, na=False) |
                df["Registration_ID"].str.lower().str.contains(search_term, na=False)
            )
            
            filtered = df[mask]
            logger.info(f"Search for '{search_term}' returned {len(filtered)} results")
            return filtered
            
        except Exception as e:
            logger.error(f"Error searching students: {str(e)}")
            return pd.DataFrame()
    
    # ==================== TUTOR OPERATIONS ====================
    
    def add_tutor(self, tutor_data: Dict) -> Tuple[bool, str]:
        """
        Add new tutor to database
        
        Args:
            tutor_data: Dictionary containing tutor information
            
        Returns:
            Tuple of (success: bool, message/tutor_id: str)
        """
        try:
            df = pd.read_excel(TUTORS_DB, engine='openpyxl')
            
            # Generate Tutor ID
            if len(df) > 0 and 'Tutor_ID' in df.columns:
                last_id = df["Tutor_ID"].max()
                if pd.notna(last_id):
                    new_id_num = int(last_id.replace('TUT', '')) + 1
                    new_id = f"TUT{new_id_num:03d}"
                else:
                    new_id = "TUT001"
            else:
                new_id = "TUT001"
            
            new_tutor = {
                "Tutor_ID": new_id,
                "Name": tutor_data.get("name", ""),
                "Email": tutor_data.get("email", "").lower(),
                "Languages_Teaching": tutor_data.get("languages", ""),
                "Available_Times": tutor_data.get("available_times", ""),
                "Contact_Number": tutor_data.get("contact", ""),
                "Date_Added": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Status": tutor_data.get("status", "Active"),
                "Specialization": tutor_data.get("specialization", ""),
                "Experience_Years": tutor_data.get("experience", 0),
                "Rating": tutor_data.get("rating", 0.0)
            }
            
            df = pd.concat([df, pd.DataFrame([new_tutor])], ignore_index=True)
            df.to_excel(TUTORS_DB, index=False, engine='openpyxl')
            
            logger.info(f"Tutor added successfully: {new_id}")
            return True, new_id
            
        except Exception as e:
            logger.error(f"Error adding tutor: {str(e)}")
            return False, str(e)
    
    def get_all_tutors(self) -> pd.DataFrame:
        """
        Get all tutors from database
        
        Returns:
            DataFrame containing all tutors
        """
        try:
            df = pd.read_excel(TUTORS_DB, engine='openpyxl')
            logger.info(f"Retrieved {len(df)} tutors from database")
            return df
        except Exception as e:
            logger.error(f"Error reading tutors database: {str(e)}")
            return pd.DataFrame()
    
    def get_tutor_by_id(self, tutor_id: str) -> Optional[pd.Series]:
        """
        Get tutor by ID
        
        Args:
            tutor_id: Tutor's ID
            
        Returns:
            Series containing tutor data or None
        """
        try:
            df = pd.read_excel(TUTORS_DB, engine='openpyxl')
            tutor = df[df["Tutor_ID"] == tutor_id]
            
            if len(tutor) > 0:
                return tutor.iloc[0]
            return None
            
        except Exception as e:
            logger.error(f"Error getting tutor {tutor_id}: {str(e)}")
            return None
    
    def get_tutor_by_email(self, email: str) -> Optional[pd.Series]:
        """
        Get tutor by email address
        
        Args:
            email: Tutor's email address
            
        Returns:
            Series containing tutor data or None
        """
        try:
            df = pd.read_excel(TUTORS_DB, engine='openpyxl')
            tutor = df[df["Email"].str.lower() == email.lower()]
            
            if len(tutor) > 0:
                return tutor.iloc[0]
            return None
            
        except Exception as e:
            logger.error(f"Error getting tutor by email {email}: {str(e)}")
            return None
    
    def get_tutor_by_name(self, name: str) -> Optional[pd.Series]:
        """
        Get tutor by name
        
        Args:
            name: Tutor's name
            
        Returns:
            Series containing tutor data or None
        """
        try:
            df = pd.read_excel(TUTORS_DB, engine='openpyxl')
            tutor = df[df["Name"] == name]
            
            if len(tutor) > 0:
                return tutor.iloc[0]
            return None
            
        except Exception as e:
            logger.error(f"Error getting tutor by name {name}: {str(e)}")
            return None
    
    def get_tutors_by_language(self, language: str) -> pd.DataFrame:
        """
        Get tutors who teach a specific language
        
        Args:
            language: Language to filter by
            
        Returns:
            DataFrame containing matching tutors
        """
        try:
            df = pd.read_excel(TUTORS_DB, engine='openpyxl')
            filtered = df[df["Languages_Teaching"].str.contains(language, na=False, case=False)]
            logger.info(f"Retrieved {len(filtered)} tutors teaching '{language}'")
            return filtered
        except Exception as e:
            logger.error(f"Error filtering tutors by language: {str(e)}")
            return pd.DataFrame()
    
    def get_active_tutors(self) -> pd.DataFrame:
        """
        Get all active tutors
        
        Returns:
            DataFrame containing active tutors
        """
        try:
            df = pd.read_excel(TUTORS_DB, engine='openpyxl')
            filtered = df[df["Status"] == "Active"]
            logger.info(f"Retrieved {len(filtered)} active tutors")
            return filtered
        except Exception as e:
            logger.error(f"Error getting active tutors: {str(e)}")
            return pd.DataFrame()
    
    def update_tutor(self, tutor_id: str, update_data: Dict) -> Tuple[bool, str]:
        """
        Update tutor record
        
        Args:
            tutor_id: Tutor's ID
            update_data: Dictionary with fields to update
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            df = pd.read_excel(TUTORS_DB, engine='openpyxl')
            idx = df[df["Tutor_ID"] == tutor_id].index
            
            if len(idx) > 0:
                for key, value in update_data.items():
                    if key in df.columns:
                        df.loc[idx[0], key] = value
                
                df.to_excel(TUTORS_DB, index=False, engine='openpyxl')
                logger.info(f"Tutor {tutor_id} updated successfully")
                return True, "Tutor updated successfully"
            else:
                logger.warning(f"Tutor {tutor_id} not found")
                return False, "Tutor not found"
                
        except Exception as e:
            logger.error(f"Error updating tutor {tutor_id}: {str(e)}")
            return False, str(e)
    
    def delete_tutor(self, tutor_id: str) -> Tuple[bool, str]:
        """
        Delete tutor record
        
        Args:
            tutor_id: Tutor's ID
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            df = pd.read_excel(TUTORS_DB, engine='openpyxl')
            initial_len = len(df)
            
            df = df[df["Tutor_ID"] != tutor_id]
            
            if len(df) < initial_len:
                df.to_excel(TUTORS_DB, index=False, engine='openpyxl')
                logger.info(f"Tutor {tutor_id} deleted successfully")
                return True, "Tutor deleted successfully"
            else:
                logger.warning(f"Tutor {tutor_id} not found for deletion")
                return False, "Tutor not found"
                
        except Exception as e:
            logger.error(f"Error deleting tutor {tutor_id}: {str(e)}")
            return False, str(e)
    
    # ==================== STATISTICS & ANALYTICS ====================
    
    def get_statistics(self) -> Dict:
        """
        Get comprehensive statistics
        
        Returns:
            Dictionary containing various statistics
        """
        try:
            students_df = self.get_all_students()
            tutors_df = self.get_all_tutors()
            
            stats = {
                "total_students": len(students_df),
                "pending_students": len(students_df[students_df["Status"] == "Pending"]),
                "approved_students": len(students_df[students_df["Status"] == "Approved"]),
                "rejected_students": len(students_df[students_df["Status"] == "Rejected"]),
                "total_tutors": len(tutors_df),
                "active_tutors": len(tutors_df[tutors_df["Status"] == "Active"]),
                "languages_distribution": students_df["Language"].value_counts().to_dict() if len(students_df) > 0 else {},
                "payment_methods": students_df["Payment_Option"].value_counts().to_dict() if len(students_df) > 0 else {},
            }
            
            logger.info("Statistics generated successfully")
            return stats
            
        except Exception as e:
            logger.error(f"Error generating statistics: {str(e)}")
            return {}
    
    def backup_database(self, backup_dir: Optional[Path] = None) -> Tuple[bool, str]:
        """
        Create backup of databases
        
        Args:
            backup_dir: Directory to store backups (default: data/backups)
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            if backup_dir is None:
                backup_dir = DATA_DIR / "backups"
            
            backup_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Backup students
            students_backup = backup_dir / f"students_backup_{timestamp}.xlsx"
            students_df = pd.read_excel(STUDENTS_DB, engine='openpyxl')
            students_df.to_excel(students_backup, index=False, engine='openpyxl')
            
            # Backup tutors
            tutors_backup = backup_dir / f"tutors_backup_{timestamp}.xlsx"
            tutors_df = pd.read_excel(TUTORS_DB, engine='openpyxl')
            tutors_df.to_excel(tutors_backup, index=False, engine='openpyxl')
            
            logger.info(f"Backup created successfully at {backup_dir}")
            return True, f"Backup created at {backup_dir}"
            
        except Exception as e:
            logger.error(f"Error creating backup: {str(e)}")
            return False, str(e)


# Utility function for testing
if __name__ == "__main__":
    db = DatabaseManager()
    print("Database Manager initialized successfully!")
    print("\nStatistics:")
    stats = db.get_statistics()
    for key, value in stats.items():
        print(f"{key}: {value}")