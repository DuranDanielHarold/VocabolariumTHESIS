"""
Email Service for Vocabolarioum
Handles all email communications including registration confirmations,
approval notifications, reminders, and general notifications
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import sys
from pathlib import Path
from typing import Dict, Tuple, Optional, List
import logging
from datetime import datetime

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config.config import EMAIL_CONFIG, CONTACT_INFO, MODULE_PDF

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailService:
    """
    Comprehensive email service for sending various types of emails
    Supports attachments, HTML formatting, and different email templates
    """
    
    def __init__(self):
        """Initialize email service with configuration"""
        self.smtp_server = EMAIL_CONFIG["smtp_server"]
        self.smtp_port = EMAIL_CONFIG["smtp_port"]
        self.sender_email = EMAIL_CONFIG["sender_email"]
        self.sender_password = EMAIL_CONFIG["sender_password"]
        logger.info("EmailService initialized")
    
    def _create_email_base(self, recipient_email: str, subject: str) -> MIMEMultipart:
        """
        Create base email structure
        
        Args:
            recipient_email: Recipient's email address
            subject: Email subject
            
        Returns:
            MIMEMultipart message object
        """
        msg = MIMEMultipart()
        msg["From"] = f"Vocabolarium <{self.sender_email}>"
        msg["To"] = recipient_email
        msg["Subject"] = subject
        return msg
    
    def _send_email(self, msg: MIMEMultipart) -> Tuple[bool, str]:
        """
        Send email using SMTP
        
        Args:
            msg: Email message to send
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {msg['To']}")
            return True, "Email sent successfully"
            
        except smtplib.SMTPAuthenticationError:
            error_msg = "Authentication failed. Check email credentials."
            logger.error(error_msg)
            return False, error_msg
            
        except smtplib.SMTPException as e:
            error_msg = f"SMTP error: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
            
        except Exception as e:
            error_msg = f"Failed to send email: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def _attach_pdf(self, msg: MIMEMultipart, pdf_path: Path, filename: Optional[str] = None) -> bool:
        """
        Attach PDF file to email
        
        Args:
            msg: Email message object
            pdf_path: Path to PDF file
            filename: Custom filename for attachment
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not pdf_path.exists():
                logger.warning(f"PDF file not found: {pdf_path}")
                return False
            
            with open(pdf_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                
                if filename is None:
                    filename = pdf_path.name
                
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {filename}"
                )
                msg.attach(part)
            
            logger.info(f"PDF attached: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Could not attach PDF: {e}")
            return False
    
    # HOTFIX: Replace the send_registration_confirmation method in utils/email_service.py

    def send_registration_confirmation(self, student_data: Dict) -> Tuple[bool, str]:
        """
        Send initial registration confirmation email with payment instructions
        
        Args:
            student_data: Dictionary containing student information
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # FIXED: Properly handle email field
            student_email = student_data.get("email", student_data.get("Email", ""))
            student_name = student_data.get("name", student_data.get("Name", ""))
            
            if not student_email:
                return False, "Student email not found in data"
            
            msg = self._create_email_base(
                student_email,
                "Vocabolarium - Registration Received"
            )
            
            # FIXED: Use .get() with fallback for all fields
            language = student_data.get("language", student_data.get("Language", ""))
            scheduled_time = student_data.get("scheduled_time", student_data.get("Scheduled_Time", ""))
            session_interval = student_data.get("session_interval", student_data.get("Session_Interval", ""))
            payment_option = student_data.get("payment_option", student_data.get("Payment_Option", ""))
            
            body = f"""
    Dear {student_name},

    Thank you for registering with Vocabolarium! 🎉

    We have received your registration for our {language} language course.

    ═══════════════════════════════════════════════════════════════
    YOUR REGISTRATION DETAILS
    ═══════════════════════════════════════════════════════════════

    📚 Language Course: {language}
    ⏰ Scheduled Time: {scheduled_time}
    📅 Session Interval: {session_interval}
    💳 Payment Method: {payment_option}
    📧 Contact Email: {student_email}

    ═══════════════════════════════════════════════════════════════
    PAYMENT INSTRUCTIONS
    ═══════════════════════════════════════════════════════════════

    Please proceed with the payment using your selected method:

    """

            # Add specific payment instructions based on method
            if payment_option == "GCash":
                body += """
    💰 GCASH PAYMENT:
    Mobile Number: 0917-123-4567
    Account Name: Maria Santos
    
    Steps:
    1. Open GCash app
    2. Select "Send Money"
    3. Enter the mobile number above
    4. Enter the course amount
    5. Take a screenshot of the payment confirmation
    6. Send the screenshot to: payments@vocabolarium.com

    """
            elif payment_option == "Bank Transfer":
                body += """
    🏦 BANK TRANSFER:
    Bank: BDO (Banco de Oro)
    Account Name: Vocabolarium Language Center
    Account Number: 1234-5678-9012
    
    Steps:
    1. Go to your bank or use online banking
    2. Transfer the course amount to the account above
    3. Keep the transaction receipt
    4. Send a photo/scan of the receipt to: payments@vocabolarium.com

    """
            elif payment_option == "PayPal":
                body += """
    💻 PAYPAL PAYMENT:
    PayPal Email: payments@vocabolarium.com
    
    Steps:
    1. Log in to your PayPal account
    2. Select "Send Money"
    3. Enter our PayPal email above
    4. Enter the course amount
    5. Take a screenshot of the payment confirmation
    6. Send the screenshot to: payments@vocabolarium.com

    """

            body += f"""
    After completing the payment, please email the receipt to:
    📧 {CONTACT_INFO["gmail"]}

    Include the following in your email:
    - Your full name: {student_name}
    - Registered email: {student_email}
    - Language course: {language}
    - Payment receipt/screenshot

    ═══════════════════════════════════════════════════════════════
    IMPORTANT REMINDERS ⚠️
    ═══════════════════════════════════════════════════════════════

    • Payment must be completed within 48 HOURS of registration
    • NO REFUNDS are allowed once payment is confirmed
    • You must STRICTLY JOIN the Google Meet link sent after approval
    • Missing classes without prior notice may result in forfeiture
    • Your registration will be reviewed within 24-48 hours after payment

    ═══════════════════════════════════════════════════════════════
    WHAT HAPPENS NEXT?
    ═══════════════════════════════════════════════════════════════

    1. ✅ Complete your payment
    2. 📧 Send payment receipt to our email
    3. ⏳ Wait for approval (24-48 hours)
    4. 🎉 Receive tutor assignment and Google Meet link
    5. 📚 Start your learning journey!

    ═══════════════════════════════════════════════════════════════
    NEED HELP?
    ═══════════════════════════════════════════════════════════════

    If you have any questions or concerns, please don't hesitate to contact us:

    📧 Email: {CONTACT_INFO["gmail"]}
    📱 Phone: {CONTACT_INFO["phone"]}
    📘 Facebook: {CONTACT_INFO["facebook"]}
    📺 YouTube: {CONTACT_INFO["youtube"]}

    We're here to help you succeed in your language learning journey!

    Best regards,
    The Vocabolarium Team
    "Connecting Cultures Through Language" 🌍

    ---
    © 2025 Vocabolarium Language Learning Center
    This is an automated message. Please do not reply directly to this email.
            """
            
            msg.attach(MIMEText(body, "plain"))
            
            return self._send_email(msg)
            
        except Exception as e:
            error_msg = f"Failed to send registration confirmation: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def send_approval_email(self, student_data: Dict, tutor_name: str, google_meet_link: str) -> Tuple[bool, str]:
        """
        Send approval email with tutor assignment and course materials
        
        Args:
            student_data: Dictionary containing student information (from DataFrame row)
            tutor_name: Assigned tutor's name
            google_meet_link: Google Meet link for classes
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Handle both dictionary and DataFrame row formats
            if hasattr(student_data, 'to_dict'):
                student_data = student_data.to_dict()
            
            msg = self._create_email_base(
                student_data.get("Email", student_data.get("email")),
                "🎉 Welcome to Vocabolarium - Registration Approved!"
            )
            
            student_name = student_data.get("Name", student_data.get("name", "Student"))
            language = student_data.get("Language", student_data.get("language", ""))
            scheduled_time = student_data.get("Scheduled_Time", student_data.get("scheduled_time", ""))
            session_interval = student_data.get("Session_Interval", student_data.get("session_interval", ""))
            
            body = f"""
Dear {student_name},

🎊 CONGRATULATIONS! Your registration has been APPROVED! 🎊

We are absolutely thrilled to welcome you to the Vocabolarium family! Get ready 
to embark on an exciting and transformative language learning journey that will 
open doors to new cultures, opportunities, and friendships.

═══════════════════════════════════════════════════════════════
YOUR COURSE INFORMATION
═══════════════════════════════════════════════════════════════

📚 Language Course: {language}
👨‍🏫 Your Assigned Tutor: {tutor_name}
⏰ Class Schedule: {scheduled_time}
📅 Session Frequency: {session_interval}
🎓 Course Duration: 1 Month (12 sessions)

═══════════════════════════════════════════════════════════════
YOUR GOOGLE MEET LINK 📹
═══════════════════════════════════════════════════════════════

Your dedicated classroom link:
{google_meet_link}

⚠️ IMPORTANT: Save this link! You'll use it for ALL your classes.

═══════════════════════════════════════════════════════════════
BEFORE YOUR FIRST CLASS
═══════════════════════════════════════════════════════════════

✅ Test your Google Meet link (click it to ensure it works)
✅ Download and review the attached course materials
✅ Prepare a notebook and pen for taking notes
✅ Ensure stable internet connection
✅ Find a quiet space for your classes
✅ Be ready 5 minutes before class time
✅ Have your camera and microphone ready

═══════════════════════════════════════════════════════════════
WHAT TO EXPECT IN YOUR CLASSES
═══════════════════════════════════════════════════════════════

🎯 Interactive Learning Sessions
   - One-on-one attention from your tutor
   - Conversational practice and real-world scenarios
   - Cultural insights and practical applications
   
📖 Comprehensive Materials
   - Course PDF (attached to this email)
   - Additional resources from your tutor
   - Practice exercises and homework
   
📊 Progress Tracking
   - Regular assessments
   - Feedback from your tutor
   - Milestone celebrations
   
🏆 Certificate Upon Completion
   - Official Vocabolarium certificate
   - Proof of language proficiency
   - Digital and printable formats

═══════════════════════════════════════════════════════════════
CLASS POLICIES & GUIDELINES
═══════════════════════════════════════════════════════════════

⏱️ PUNCTUALITY
   - Classes start ON TIME
   - Late arrivals will not extend the session
   - Be ready 5 minutes early

📵 ATTENDANCE
   - Notify tutor 24 hours in advance if you can't attend
   - Maximum 2 excused absences per month
   - Missed classes without notice cannot be made up

🎥 PARTICIPATION
   - Camera must be ON during classes
   - Active participation is encouraged
   - Complete assigned homework

🚫 CODE OF CONDUCT
   - Respect your tutor and class time
   - No recording without permission
   - Professional and courteous behavior

═══════════════════════════════════════════════════════════════
LEARNING TIPS FOR SUCCESS 💡
═══════════════════════════════════════════════════════════════

1. Practice daily, even if just for 10 minutes
2. Immerse yourself in the language (music, movies, podcasts)
3. Don't be afraid to make mistakes - they're part of learning!
4. Ask questions whenever you don't understand
5. Review materials before and after each class
6. Set personal learning goals and track progress
7. Connect with language communities online

═══════════════════════════════════════════════════════════════
COURSE MATERIALS 📚
═══════════════════════════════════════════════════════════════

Your {language} course materials are attached to this email. Please:
• Download and save them to your device
• Print them if you prefer physical copies
• Review them before your first class
• Bring them to every session

═══════════════════════════════════════════════════════════════
MEET YOUR TUTOR: {tutor_name}
═══════════════════════════════════════════════════════════════

Your tutor has been carefully selected based on:
✓ Language expertise and teaching experience
✓ Your schedule compatibility
✓ Teaching style that matches your learning needs

Your tutor will contact you soon to:
• Introduce themselves
• Discuss your learning goals
• Answer any questions you may have
• Schedule your first class

═══════════════════════════════════════════════════════════════
NEED SUPPORT? WE'RE HERE FOR YOU! 🤝
═══════════════════════════════════════════════════════════════

Have questions? Technical issues? Need to reschedule?
Contact us anytime:

📧 Email: {CONTACT_INFO["gmail"]}
📱 Phone/SMS: {CONTACT_INFO["phone"]}
📘 Facebook: {CONTACT_INFO["facebook"]}
📺 YouTube: {CONTACT_INFO["youtube"]}

Response time: Within 24 hours

═══════════════════════════════════════════════════════════════
STAY CONNECTED
═══════════════════════════════════════════════════════════════

Follow us on social media for:
• Learning tips and resources
• Student success stories
• Cultural insights
• Special promotions
• Language learning community

📘 Facebook: {CONTACT_INFO["facebook"]}
📺 YouTube: {CONTACT_INFO["youtube"]}

═══════════════════════════════════════════════════════════════

We're excited to be part of your language learning journey! Your dedication 
and enthusiasm, combined with our expert instruction, will help you achieve 
your language goals.

Remember: Every expert was once a beginner. You've taken the first step, 
and we'll be with you every step of the way! 🌟

Let's make this an amazing learning experience together!

Best regards,
The Vocabolarium Team
"Connecting Cultures Through Language" 🌍

---
P.S. Don't forget to test your Google Meet link and review your materials 
before your first class!

© 2025 Vocabolarium Language Learning Center
For support: {CONTACT_INFO["gmail"]} | {CONTACT_INFO["phone"]}
            """
            
            msg.attach(MIMEText(body, "plain"))
            
            # Attach PDF materials if they exist
            if MODULE_PDF.exists():
                self._attach_pdf(msg, MODULE_PDF, f"{language}_Course_Materials.pdf")
            else:
                logger.warning(f"Course materials PDF not found at {MODULE_PDF}")
            
            return self._send_email(msg)
            
        except Exception as e:
            error_msg = f"Failed to send approval email: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def send_rejection_email(self, student_data: Dict, reason: Optional[str] = None) -> Tuple[bool, str]:
        """
        Send rejection email to student
        
        Args:
            student_data: Dictionary containing student information
            reason: Optional rejection reason
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            if hasattr(student_data, 'to_dict'):
                student_data = student_data.to_dict()
            
            msg = self._create_email_base(
                student_data.get("Email", student_data.get("email")),
                "Vocabolarium - Registration Update"
            )
            
            student_name = student_data.get("Name", student_data.get("name", "Student"))
            
            body = f"""
Dear {student_name},

Thank you for your interest in Vocabolarium Language Learning Center.

After careful review of your registration, we regret to inform you that we 
are unable to process your application at this time.

"""
            
            if reason:
                body += f"""
Reason: {reason}

"""
            
            body += f"""
We appreciate your interest and encourage you to:
• Contact us for more information
• Reapply when circumstances change
• Explore our other language offerings

If you have any questions, please contact us:
📧 Email: {CONTACT_INFO["gmail"]}
📱 Phone: {CONTACT_INFO["phone"]}

Thank you for considering Vocabolarium.

Best regards,
The Vocabolarium Team

---
© 2025 Vocabolarium Language Learning Center
            """
            
            msg.attach(MIMEText(body, "plain"))
            
            return self._send_email(msg)
            
        except Exception as e:
            error_msg = f"Failed to send rejection email: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def send_reminder_email(self, student_email: str, student_name: str, class_time: str, google_meet_link: str) -> Tuple[bool, str]:
        """
        Send class reminder email
        
        Args:
            student_email: Student's email
            student_name: Student's name
            class_time: Class schedule time
            google_meet_link: Google Meet link
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            msg = self._create_email_base(
                student_email,
                "⏰ Class Reminder - Vocabolarium"
            )
            
            body = f"""
Dear {student_name},

This is a friendly reminder about your upcoming class!

⏰ Class Time: {class_time}
📹 Google Meet Link: {google_meet_link}

Please join a few minutes early to ensure everything is working properly.

See you in class!

Best regards,
The Vocabolarium Team

---
© 2025 Vocabolarium Language Learning Center
            """
            
            msg.attach(MIMEText(body, "plain"))
            
            return self._send_email(msg)
            
        except Exception as e:
            error_msg = f"Failed to send reminder email: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def send_test_email(self, recipient_email: str) -> Tuple[bool, str]:
        """
        Send test email to verify configuration
        
        Args:
            recipient_email: Email address to send test to
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            msg = self._create_email_base(
                recipient_email,
                "Vocabolarium - Email Service Test"
            )
            
            body = f"""
This is a test email from Vocabolarium Email Service.

If you received this email, the email configuration is working correctly! ✅

Test Details:
- Sent at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- SMTP Server: {self.smtp_server}
- SMTP Port: {self.smtp_port}
- Sender: {self.sender_email}

Best regards,
Vocabolarium Team

---
© 2025 Vocabolarium Language Learning Center
            """
            
            msg.attach(MIMEText(body, "plain"))
            
            return self._send_email(msg)
            
        except Exception as e:
            error_msg = f"Failed to send test email: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def send_bulk_email(self, recipients: List[str], subject: str, body: str) -> Tuple[int, int]:
        """
        Send email to multiple recipients
        
        Args:
            recipients: List of email addresses
            subject: Email subject
            body: Email body
            
        Returns:
            Tuple of (successful_count: int, failed_count: int)
        """
        successful = 0
        failed = 0
        
        for recipient in recipients:
            try:
                msg = self._create_email_base(recipient, subject)
                msg.attach(MIMEText(body, "plain"))
                success, _ = self._send_email(msg)
                
                if success:
                    successful += 1
                else:
                    failed += 1
                    
            except Exception as e:
                logger.error(f"Failed to send bulk email to {recipient}: {str(e)}")
                failed += 1
        
        logger.info(f"Bulk email complete: {successful} successful, {failed} failed")
        return successful, failed


# Utility function for testing
if __name__ == "__main__":
    email_service = EmailService()
    print("Email Service initialized successfully!")
    print(f"SMTP Server: {email_service.smtp_server}")
    print(f"SMTP Port: {email_service.smtp_port}")
    print(f"Sender Email: {email_service.sender_email}")