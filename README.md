# 🌍 VOCABOLARIOUM - Language Learning Platform

A comprehensive language registration and management system built with Streamlit. This platform enables students to register for language courses and provides administrators with powerful tools to manage students, tutors, and approvals.

## 📋 Table of Contents

- [Features](#features)
- [System Requirements](#system-requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [User Guide](#user-guide)
- [Admin Guide](#admin-guide)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

## ✨ Features

### Student Features
- **Interactive Hero Page**: Engaging landing page with language offerings
- **Language Programs**: Korean, Japanese, Mandarin, English, and Filipino
- **Easy Registration**: Simple form-based registration process
- **Automated Emails**: Confirmation and approval emails with course materials
- **Flexible Scheduling**: Choose preferred time slots and session frequency

### Admin Features
- **Dashboard Overview**: Statistics and analytics at a glance
- **Student Management**: Full CRUD operations for student records
- **Tutor Management**: Manage tutor database
- **Approval System**: Approve/reject registrations with email notifications
- **Data Export**: Export student and tutor data to CSV
- **Email Testing**: Test email configuration

## 🔧 System Requirements

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (venv)
- Gmail account with App Password (for email functionality)

## 📥 Installation

### Step 1: Clone or Download the Project

Create the project directory structure:

```bash
mkdir vocabolarioum
cd vocabolarioum
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

Create `requirements.txt` and install:

```bash
pip install -r requirements.txt
```

### Step 4: Create Directory Structure

```bash
# Create necessary directories
mkdir -p config data assets/languages utils pages

# Create empty __init__.py files
touch utils/__init__.py
```

### Step 5: Set Up Configuration Files

Place all the provided Python files in their respective directories:

```
vocabolarioum/
├── app.py
├── config/
│   └── config.py
├── utils/
│   ├── __init__.py
│   ├── database.py
│   ├── email_service.py
│   └── auth.py
├── pages/
│   ├── 1_🏠_Home.py
│   ├── 2_📝_Registration.py
│   └── 3_👨‍💼_Admin_Dashboard.py
├── data/
│   ├── students.xlsx (auto-created)
│   └── tutors.xlsx (auto-created)
└── assets/
    └── languages/
        └── module.pdf (add your PDF here)
```

## ⚙️ Configuration

### Email Configuration

To enable email functionality, you need to configure Gmail App Password:

1. Go to your Google Account settings
2. Enable 2-Factor Authentication
3. Generate an App Password:
   - Go to Security → App Passwords
   - Select "Mail" and "Other"
   - Copy the generated password

4. Set environment variables:

**On Windows (Command Prompt):**
```cmd
set SENDER_EMAIL=your-email@gmail.com
set EMAIL_PASSWORD=your-app-password
```

**On Windows (PowerShell):**
```powershell
$env:SENDER_EMAIL="your-email@gmail.com"
$env:EMAIL_PASSWORD="your-app-password"
```

**On macOS/Linux:**
```bash
export SENDER_EMAIL="your-email@gmail.com"
export EMAIL_PASSWORD="your-app-password"
```

### Create .env File (Optional but Recommended)

Create a `.env` file in the root directory:

```env
SENDER_EMAIL=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
ADMIN_USER=admin
ADMIN_PASS=admin123
```

Then install python-dotenv (already in requirements.txt) and modify config.py to load from .env:

```python
from dotenv import load_dotenv
load_dotenv()
```

### Admin Credentials

Default admin credentials:
- **Username**: admin
- **Password**: admin123

**⚠️ IMPORTANT**: Change these credentials in production!

## 🚀 Running the Application

### Start the Application

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Access Different Pages

- **Home/Hero Page**: Automatic redirect or navigate from welcome screen
- **Registration**: Click "Inquire Now" on any language or use navigation
- **Admin Dashboard**: Click "Admin Login" and use credentials

## 📖 User Guide

### For Students

1. **Browse Languages**
   - Visit the Home page
   - Explore available language programs
   - Click on each language to see detailed information

2. **Register for a Course**
   - Click "Inquire Now" on your desired language
   - Fill in all required information:
     - Full Name
     - Email Address
     - Age
     - Preferred Time Slot
     - Sessions Per Week
     - Payment Method
   - Accept terms and conditions
   - Submit the form

3. **After Registration**
   - Check your email for confirmation
   - Follow payment instructions
   - Send payment receipt to the provided email
   - Wait for approval (24-48 hours)

4. **After Approval**
   - Receive welcome email with:
     - Assigned tutor details
     - Google Meet link
     - Course materials (PDF)
     - Schedule information

## 👨‍💼 Admin Guide

### Logging In

1. Navigate to Admin Dashboard
2. Enter credentials (admin/admin123)
3. Click Login

### Managing Students

#### View Students
- Go to "Student Management" tab
- Use filters to sort by status or language
- View all student details in the table

#### Approve a Student
1. Select student from dropdown
2. Choose "Approve" action
3. Assign a tutor
4. Enter Google Meet link (auto-generated)
5. Click "Approve & Send Email"
6. Student receives approval email automatically

#### Reject a Student
1. Select student from dropdown
2. Choose "Reject" action
3. Optionally enter rejection reason
4. Confirm rejection

#### Edit Student Information
1. Select student from dropdown
2. Choose "Edit" action
3. Modify required fields
4. Save changes

#### Delete Student Record
1. Select student from dropdown
2. Choose "Delete" action
3. Confirm deletion (cannot be undone)

### Managing Tutors

#### Add New Tutor
1. Go to "Tutor Management" tab
2. Fill in tutor information:
   - Name
   - Email
   - Contact Number
   - Languages Teaching
   - Available Times
3. Click "Add Tutor"

#### Edit/Delete Tutors
- Select tutor from dropdown
- Choose desired action
- Follow prompts

### Export Data

1. Go to "Settings" tab
2. Click "Export Students Data" or "Export Tutors Data"
3. Download CSV file

### Test Email Service

1. Go to "Settings" tab
2. Enter test email address
3. Click "Send Test Email"
4. Check if email is received

## 📁 Project Structure

```
vocabolarioum/
│
├── app.py                          # Main application entry point
│
├── config/
│   └── config.py                   # Configuration settings
│
├── utils/
│   ├── __init__.py                 # Package initialization
│   ├── database.py                 # Database operations
│   ├── email_service.py            # Email functionality
│   └── auth.py                     # Authentication utilities
│
├── pages/
│   ├── 1_🏠_Home.py               # Hero/Inquiring page
│   ├── 2_📝_Registration.py       # Registration form
│   └── 3_👨‍💼_Admin_Dashboard.py  # Admin panel
│
├── data/
│   ├── students.xlsx               # Student database (auto-created)
│   └── tutors.xlsx                 # Tutor database (auto-created)
│
├── assets/
│   ├── styles.css                  # Custom CSS (optional)
│   └── languages/
│       └── module.pdf              # Language learning materials
│
├── venv/                           # Virtual environment
│
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🔍 Troubleshooting

### Email Not Sending

**Problem**: Registration emails are not being sent

**Solutions**:
1. Verify Gmail App Password is correct
2. Check environment variables are set
3. Ensure 2FA is enabled on Google account
4. Test email service in Admin Dashboard
5. Check spam/junk folder

**Alternative**: If email fails, system still saves registration and shows warning

### Database Errors

**Problem**: Excel files not found or corrupted

**Solutions**:
1. Delete `data/students.xlsx` and `data/tutors.xlsx`
2. Restart application (files will be recreated)
3. Ensure write permissions in data directory

### Import Errors

**Problem**: Module not found errors

**Solutions**:
1. Ensure virtual environment is activated
2. Reinstall dependencies: `pip install -r requirements.txt`
3. Check Python path in imports
4. Verify all files are in correct directories

### Port Already in Use

**Problem**: Port 8501 is already in use

**Solution**:
```bash
# Use a different port
streamlit run app.py --server.port 8502
```

### Streamlit Navigation Issues

**Problem**: Pages not switching correctly

**Solutions**:
1. Clear browser cache
2. Use Streamlit's built-in navigation in sidebar
3. Restart the application
4. Try a different browser

## 🎨 Customization

### Changing Languages

Edit `config/config.py` → `LANGUAGES` dictionary:

```python
LANGUAGES = {
    "Your Language": {
        "description": "Your description",
        "culture": "Cultural information",
        "origin": "Historical origin",
        "price": "₱X,XXX/month",
        "sessions": "XX sessions per month",
    }
}
```

### Modifying Email Templates

Edit `utils/email_service.py`:
- `send_registration_confirmation()` - Initial confirmation email
- `send_approval_email()` - Approval email with tutor assignment

### Changing Color Scheme

Edit CSS in each page file to modify colors:
- Primary: `#667eea`
- Secondary: `#764ba2`
- Success: `#28a745`
- Warning: `#ffc107`

### Adding New Payment Options

Edit `config/config.py` → `PAYMENT_OPTIONS`:

```python
PAYMENT_OPTIONS = ["GCash", "Bank Transfer", "PayPal", "Credit Card"]
```

## 📊 Database Schema

### Students Table (students.xlsx)

| Column | Type | Description |
|--------|------|-------------|
| Registration_ID | String | Unique identifier (REG0001, REG0002, ...) |
| Name | String | Student full name |
| Email | String | Student email address |
| Age | Integer | Student age |
| Language | String | Selected language course |
| Scheduled_Time | String | Preferred class time |
| Session_Interval | String | Sessions per week |
| Payment_Option | String | Chosen payment method |
| Registration_Date | DateTime | When registered |
| Status | String | Pending/Approved/Rejected |
| Assigned_Tutor | String | Tutor name (after approval) |
| Google_Meet_Link | String | Meeting link (after approval) |

### Tutors Table (tutors.xlsx)

| Column | Type | Description |
|--------|------|-------------|
| Tutor_ID | String | Unique identifier (TUT001, TUT002, ...) |
| Name | String | Tutor full name |
| Email | String | Tutor email address |
| Languages_Teaching | String | Comma-separated languages |
| Available_Times | String | Available time slots |
| Contact_Number | String | Phone number |
| Date_Added | DateTime | When added to system |

## 🔐 Security Considerations

### For Development
- Default credentials are acceptable
- Email credentials via environment variables
- Local database (Excel files)

### For Production
1. **Change Admin Credentials**
   - Use strong passwords
   - Implement proper authentication (OAuth, JWT)
   
2. **Secure Email Configuration**
   - Use environment variables
   - Never commit credentials to version control
   
3. **Database Security**
   - Consider migrating to PostgreSQL/MySQL
   - Implement proper access controls
   - Regular backups
   
4. **HTTPS**
   - Deploy behind reverse proxy (nginx)
   - Use SSL certificates
   
5. **Input Validation**
   - Sanitize all user inputs
   - Implement rate limiting
   - Add CAPTCHA for registration

## 🚀 Deployment

### Deploy to Streamlit Cloud

1. Push code to GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select repository and branch
5. Add secrets in Streamlit Cloud dashboard:
   ```
   SENDER_EMAIL = "your-email@gmail.com"
   EMAIL_PASSWORD = "your-app-password"
   ADMIN_USER = "admin"
   ADMIN_PASS = "your-secure-password"
   ```
6. Deploy

### Deploy to Heroku

1. Create `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Create `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

3. Deploy to Heroku:
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

### Deploy to VPS (Ubuntu)

1. Install dependencies:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv nginx
   ```

2. Set up application:
   ```bash
   cd /var/www
   git clone your-repo
   cd vocabolarioum
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Create systemd service:
   ```bash
   sudo nano /etc/systemd/system/vocabolarioum.service
   ```
   
   ```ini
   [Unit]
   Description=Vocabolarioum Streamlit App
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/var/www/vocabolarioum
   Environment="PATH=/var/www/vocabolarioum/venv/bin"
   ExecStart=/var/www/vocabolarioum/venv/bin/streamlit run app.py

   [Install]
   WantedBy=multi-user.target
   ```

4. Start service:
   ```bash
   sudo systemctl start vocabolarioum
   sudo systemctl enable vocabolarioum
   ```

## 📝 License

This project is created for educational and commercial use. Modify as needed for your organization.

## 🤝 Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues or questions:

- **Email**: vocabolarioum@gmail.com
- **Phone**: +63 917 123 4567
- **Facebook**: @vocabolarioum

## 🎯 Future Enhancements

- [ ] Real-time chat support
- [ ] Student progress tracking
- [ ] Video lesson library
- [ ] Mobile app version
- [ ] Multi-language interface
- [ ] Payment gateway integration
- [ ] Certificate generation
- [ ] Student dashboard
- [ ] Tutor scheduling system
- [ ] Automated reminders via SMS

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Gmail API Documentation](https://developers.google.com/gmail/api)

---

**Built with ❤️ using Streamlit**

*Version 1.0.0 - October 2025*