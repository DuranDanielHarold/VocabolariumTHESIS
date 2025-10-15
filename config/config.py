"""
Configuration file for Vocabolarioum Language Learning Platform
Contains all application settings, paths, and constants
"""

import os
from pathlib import Path
from typing import Dict, List

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# ==================== BASE PATHS ====================

# Base directory - root of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Database paths
DATA_DIR = BASE_DIR / "data"
STUDENTS_DB = DATA_DIR / "students.xlsx"
TUTORS_DB = DATA_DIR / "tutors.xlsx"

# Assets paths
ASSETS_DIR = BASE_DIR / "assets"
LANGUAGES_DIR = ASSETS_DIR / "languages"
MODULE_PDF = LANGUAGES_DIR / "module.pdf"

# Backup directory
BACKUP_DIR = DATA_DIR / "backups"


# ==================== EMAIL CONFIGURATION ====================

# Email configuration (use environment variables in production)
EMAIL_CONFIG = {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": os.getenv("SENDER_EMAIL", "lbtmoticketsystem@gmail.com"),
    "sender_password": os.getenv("EMAIL_PASSWORD", "opkquepefebmxlec"),
}


# ==================== USER CREDENTIALS & ROLES ====================

# Admin credentials (use environment variables in production)
ADMIN_USERNAME = os.getenv("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASS", "admin123")

# User roles
USER_ROLES = {
    "admin": "Administrator",
    "tutor": "Tutor"
}

# Tutor login credentials (email-based)
# Tutors use their email from tutors.xlsx to login
# Default password for all tutors (they should change this)
DEFAULT_TUTOR_PASSWORD = "tutor123"

# User credentials database (for demo - in production use proper auth)
USER_CREDENTIALS = {
    "admin": {
        "password": ADMIN_PASSWORD,
        "role": "admin",
        "name": "System Administrator"
    },
    # Tutors will be loaded dynamically from tutors.xlsx
}


# ==================== LANGUAGE OFFERINGS ====================

# Detailed information about each language course
LANGUAGES: Dict[str, Dict[str, str]] = {
    "Korean": {
        "description": "Learn the beautiful Korean language, essential for K-pop, K-dramas, and Korean business culture. Korean (한국어) evolved from Old Korean and uses the unique Hangul alphabet created in 1443 by King Sejong the Great. It's spoken by 77 million people worldwide and is the gateway to understanding one of Asia's most dynamic cultures.",
        "culture": "Korean culture emphasizes respect (jeong), family values, and technological innovation. The language reflects hierarchical social structures through honorifics and various speech levels. From traditional hanbok to modern K-culture, learning Korean opens doors to understanding this rich heritage.",
        "origin": "Korean originated from Proto-Koreanic languages around 2000 BCE and developed through the Three Kingdoms period. The language has been influenced by Chinese characters (Hanja) but maintains its unique grammatical structure and alphabet system.",
        "price": "₱7,000/2 month",
        "sessions": "12 sessions per month",
        "icon": "🇰🇷",
        "difficulty": "Medium",
        "popularity": "Very High"
    },
    "Japanese": {
        "description": "Master Japanese, the gateway to anime, manga, and Japanese business opportunities. Japanese (日本語) uses three writing systems: Hiragana, Katakana, and Kanji. Spoken by 125 million people, it's essential for understanding Japan's unique blend of ancient tradition and cutting-edge technology.",
        "culture": "Japanese culture values harmony (wa), respect, and precision. The language reflects these through complex politeness levels (keigo) and context-dependent expressions. From tea ceremonies to anime, Japanese offers insight into a fascinating culture.",
        "origin": "Japanese evolved from Japonic languages, influenced by Chinese in the 5th century CE, developing unique grammatical structures and writing systems. The language has absorbed elements from various cultures while maintaining its distinctive character.",
        "price": "₱7,000/2 month",
        "sessions": "12 sessions per month",
        "icon": "🇯🇵",
        "difficulty": "Hard",
        "popularity": "Very High"
    },
    "Mandarin": {
        "description": "Unlock opportunities with Mandarin, the most spoken language globally. Mandarin Chinese (普通话) is spoken by over 1 billion people and is crucial for business in Asia. Master the tonal pronunciation and logographic characters to access one of the world's oldest continuous civilizations.",
        "culture": "Chinese culture spans 5,000 years with rich traditions in philosophy, arts, and family values. The language uses tonal pronunciation and logographic characters, each carrying deep historical and cultural significance. Understanding Mandarin means understanding global business and ancient wisdom.",
        "origin": "Mandarin evolved from Middle Chinese around the 14th century, becoming the official language based on the Beijing dialect. The standardized form (Putonghua) is now used throughout China and is one of the six official UN languages.",
        "price": "₱7,000/2 month",
        "sessions": "12 sessions per month",
        "icon": "🇨🇳",
        "difficulty": "Hard",
        "popularity": "High"
    },
    "English": {
        "description": "Perfect your English skills for global communication, business, and academic success. English is the international language of business and education, spoken by 1.5 billion people worldwide. From Shakespeare to Silicon Valley, English dominates global discourse and opportunity.",
        "culture": "English culture emphasizes individualism, direct communication, and innovation. The language has become the global lingua franca, facilitating international business, science, technology, and diplomacy. English proficiency opens doors worldwide.",
        "origin": "English originated from Anglo-Saxon dialects in 5th century Britain, evolving through Norman French influence into Modern English. Today's English incorporates vocabulary from hundreds of languages, making it rich and adaptable.",
        "price": "₱7,000/2 month",
        "sessions": "12 sessions per month",
        "icon": "🇬🇧",
        "difficulty": "Medium",
        "popularity": "Very High"
    },
    "Filipino": {
        "description": "Strengthen your Filipino language skills and connect with Philippine culture. Filipino (based on Tagalog) is the national language of the Philippines, spoken by 45 million native speakers and understood by over 100 million. It's the language of bayanihan, malasakit, and pakikipagkapwa.",
        "culture": "Filipino culture blends indigenous, Spanish, and American influences, emphasizing family (pamilya), hospitality (pakikipagkapwa-tao), and community (bayanihan). The language carries the warmth and resilience of the Filipino spirit.",
        "origin": "Filipino evolved from Old Tagalog, influenced by Sanskrit, Malay, Spanish, and English throughout Philippine history. Declared the national language in 1987, it continues to evolve while preserving indigenous roots.",
        "price": "₱7,000/2 month",
        "sessions": "12 sessions per month",
        "icon": "🇵🇭",
        "difficulty": "Easy",
        "popularity": "Medium"
    },
}


# ==================== SESSION & PAYMENT OPTIONS ====================

# Available session intervals per week
SESSION_INTERVALS: List[str] = [
    "2 times per week",
    "3 times per week",
    "4 times per week",
    "5 times per week"
]

# Available time slots for classes
TIME_SLOTS: List[str] = [
    "10:00 AM - 1:00 PM"
]

# Payment options available
PAYMENT_OPTIONS: List[str] = [
    "GCash",
    "Bank Transfer",
]

# Payment details for each method
PAYMENT_DETAILS: Dict[str, Dict[str, str]] = {
    "GCash": {
        "number": "09069481145",
        "name": "LeeAnn Librada",
        "instructions": "Send money via GCash app, take screenshot, and email to payments@vocabolarium.com"
    },
    "Bank Transfer": {
        "bank": "BDO (Banco de Oro)",
        "account_name": "LeeAnn Librada",
        "account_number": "09069481145",
        "instructions": "Transfer to the account above and send receipt to payments@vocabolarium.com"
    },
    "PayPal": {
        "email": "payments@vocabolarium.com",
        "instructions": "Send payment to our PayPal email and send screenshot to payments@vocabolarium.com"
    }
}


# ==================== CONTACT INFORMATION ====================

# Official contact information
CONTACT_INFO: Dict[str, str] = {
    "email": "vocabolarium@gmail.com",
    "gmail": "vocabolarium@gmail.com",
    "payment_email": "payments@vocabolarium.com",
    "phone": "+63 917 123 4567",
    "facebook": "https://facebook.com/vocabolarium",
    "youtube": "https://youtube.com/@vocabolarium",
    "address": "123 Education St., Paranaque City, Metro Manila, Philippines"
}


# ==================== APPLICATION SETTINGS ====================

# Application metadata
APP_NAME = "Vocabolarium"
APP_VERSION = "1.1.0"
APP_DESCRIPTION = "Language Learning Platform - Connecting Cultures Through Language"
APP_AUTHOR = "Vocabolarium Development Team"

# Session configuration
SESSION_DURATION_HOURS = 8  # How long sessions last
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 15

# Registration settings
PAYMENT_DEADLINE_HOURS = 48  # Hours to complete payment after registration
APPROVAL_PROCESSING_HOURS = 48  # Expected approval time

# Student statuses
STUDENT_STATUSES: List[str] = [
    "Pending",
    "Approved",
    "Rejected",
    "Active",
    "Completed",
    "Suspended"
]

# Tutor statuses
TUTOR_STATUSES: List[str] = [
    "Active",
    "Inactive",
    "On Leave"
]


# ==================== UI THEME SETTINGS ====================

# Color scheme for the application
THEME_COLORS: Dict[str, str] = {
    "primary": "#667eea",
    "secondary": "#764ba2",
    "success": "#28a745",
    "warning": "#ffc107",
    "danger": "#dc3545",
    "info": "#17a2b8",
    "light": "#f8f9fa",
    "dark": "#343a40"
}

# Gradients
GRADIENTS: Dict[str, str] = {
    "primary": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
    "success": "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)",
    "warning": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
    "ocean": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
}


# ==================== FEATURES & BENEFITS ====================

# Platform features for marketing
PLATFORM_FEATURES: List[Dict[str, str]] = [
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
    },
    {
        "icon": "🎓",
        "title": "Expert Tutors",
        "description": "Learn from certified native or near-native speakers with years of teaching experience."
    },
    {
        "icon": "💻",
        "title": "Online Classes",
        "description": "Learn from anywhere via Google Meet. No need to commute, just log in and learn!"
    },
    {
        "icon": "📚",
        "title": "Quality Materials",
        "description": "Comprehensive PDF modules, exercises, and resources to support your learning journey."
    }
]


# ==================== VALIDATION RULES ====================

# Validation settings
VALIDATION_RULES: Dict[str, any] = {
    "min_age": 5,
    "max_age": 100,
    "min_name_length": 3,
    "max_name_length": 100,
    "email_pattern": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    "phone_pattern": r'^\+?[\d\s-]{10,}$'
}


# ==================== GOOGLE MEET CONFIGURATION ====================

# Google Meet link templates
GOOGLE_MEET_TEMPLATE = "https://meet.google.com/{code}"
GOOGLE_MEET_CODE_LENGTH = 10


# ==================== DATABASE CONFIGURATION ====================

# Database column definitions for reference
STUDENTS_COLUMNS: List[str] = [
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
]

TUTORS_COLUMNS: List[str] = [
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
]


# ==================== UTILITY FUNCTIONS ====================

def get_language_list() -> List[str]:
    """Get list of available languages"""
    return list(LANGUAGES.keys())


def get_language_info(language: str) -> Dict[str, str]:
    """Get information about a specific language"""
    return LANGUAGES.get(language, {})


def is_valid_email(email: str) -> bool:
    """Validate email format"""
    import re
    return bool(re.match(VALIDATION_RULES["email_pattern"], email))


def is_valid_age(age: int) -> bool:
    """Validate age"""
    return VALIDATION_RULES["min_age"] <= age <= VALIDATION_RULES["max_age"]


# ==================== EXPORT SETTINGS ====================

# What to export when using 'from config import *'
__all__ = [
    'BASE_DIR',
    'DATA_DIR',
    'STUDENTS_DB',
    'TUTORS_DB',
    'MODULE_PDF',
    'EMAIL_CONFIG',
    'ADMIN_USERNAME',
    'ADMIN_PASSWORD',
    'DEFAULT_TUTOR_PASSWORD',
    'USER_ROLES',
    'LANGUAGES',
    'SESSION_INTERVALS',
    'PAYMENT_OPTIONS',
    'CONTACT_INFO',
    'APP_NAME',
    'APP_VERSION',
    'THEME_COLORS',
    'PLATFORM_FEATURES',
    'VALIDATION_RULES'
]


# Print confirmation when loaded
if __name__ == "__main__":
    print(f"✅ {APP_NAME} v{APP_VERSION} Configuration Loaded")
    print(f"📁 Base Directory: {BASE_DIR}")
    print(f"💾 Students DB: {STUDENTS_DB}")
    print(f"👨‍🏫 Tutors DB: {TUTORS_DB}")
    print(f"🌍 Languages Available: {', '.join(LANGUAGES.keys())}")
    print(f"📧 Email Configured: {EMAIL_CONFIG['sender_email']}")
    print(f"🔐 Admin User: {ADMIN_USERNAME}")