#pip install schedule
# pip install twilio
import datetime
import smtplib
from email.mime.text import MIMEText
import schedule
import time

# Store all appointment details in a structured format (list of dictionaries)

appointments = [
    {
        "patient_name": "Agu Miracle",
        "doctor_name": "Dr. Strange",
        "patient_contact": "+2348134814891",
        "doctor_contact": "+2348103481560",
        "datetime": datetime.datetime(2025, 5, 25, 14, 30),
        "channel": "email",  # could be 'sms', 'whatsapp', etc.
        "patient_email": "Agu803eh@gmail.com",
        "doctor_email": "ogunsanya.abdulgafar@gmail.com"
    },
    {
        "patient_name": "John Wick",
        "doctor_name": "Dr. Smith",
        "patient_contact": "+2349012345678",
        "doctor_contact": "+2349087654321",
        "datetime": datetime.datetime(2025, 5, 26, 10, 0),
        "channel": "sms",  # could be 'email', 'whatsapp', etc.
        "patient_email": "Johnwick@gmail.com",
        "doctor_email": "Smith12687@gmail.com"
    },

    # Add more appointments as needed
]

def send_email(to_email, subject, body):
    # Configure your SMTP server here
    smtp_server = "smtp.example.com"
    smtp_port = 587
    smtp_user = "your_email@example.com"
    smtp_password = "your_password"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = to_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, [to_email], msg.as_string())
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

def remind_appointments():
    now = datetime.datetime.now()
    for appt in appointments:
        # Send reminder 1 day before appointment
        if 0 <= (appt["datetime"] - now).days <= 1:
            subject = f"Appointment Reminder: {appt['datetime'].strftime('%Y-%m-%d %H:%M')}"
            patient_body = f"Dear {appt['patient_name']},\nThis is a reminder for your appointment with {appt['doctor_name']} on {appt['datetime']}."
            doctor_body = f"Dear {appt['doctor_name']},\nThis is a reminder for your appointment with {appt['patient_name']} on {appt['datetime']}."
            if appt["channel"] == "email":
                send_email(appt["patient_email"], subject, patient_body)
                send_email(appt["doctor_email"], subject, doctor_body)
            # For SMS/WhatsApp, integrate with Twilio or other APIs here

if __name__ == "__main__":
    remind_appointments()
    # Schedule the remind_appointments function to run every hour
    schedule.every(1).hours.do(remind_appointments)

    print("Scheduler started. Press Ctrl+C to exit.")
    while True:
        schedule.run_pending()
        time.sleep(1)
        # Mark appointments as reminded to avoid duplicate reminders
        reminded_appointments = set()

        def remind_appointments():
            now = datetime.datetime.now()
            for idx, appt in enumerate(appointments):
                # Skip if already reminded
                if idx in reminded_appointments:
                    continue
                # Send reminder 1 day before appointment
                if 0 <= (appt["datetime"] - now).days <= 1:
                    subject = f"Appointment Reminder: {appt['datetime'].strftime('%Y-%m-%d %H:%M')}"
                    patient_body = f"Dear {appt['patient_name']},\nThis is a reminder for your appointment with {appt['doctor_name']} on {appt['datetime']}."
                    doctor_body = f"Dear {appt['doctor_name']},\nThis is a reminder for your appointment with {appt['patient_name']} on {appt['datetime']}."
                    if appt["channel"] == "email":
                        send_email(appt["patient_email"], subject, patient_body)
                        send_email(appt["doctor_email"], subject, doctor_body)
                    # Mark as reminded
                    reminded_appointments.add(idx)

                    # Function to process responses (accept/decline)
                    def process_response(appointment_idx, responder, response):
                        appt = appointments[appointment_idx]
                        if "responses" not in appt:
                            appt["responses"] = {}
                        appt["responses"][responder] = response
                        print(f"{responder} responded '{response}' for appointment on {appt['datetime']}.")

                    # Example: Simulate user input for accepting/declining
                    def prompt_for_response():
                        for idx, appt in enumerate(appointments):
                            if "responses" not in appt or "patient" not in appt["responses"]:
                                resp = input(f"{appt['patient_name']}, do you accept the appointment with {appt['doctor_name']} on {appt['datetime']}? (accept/decline): ")
                                process_response(idx, "patient", resp.strip().lower())
                            if "responses" not in appt or "doctor" not in appt["responses"]:
                                resp = input(f"{appt['doctor_name']}, do you accept the appointment with {appt['patient_name']} on {appt['datetime']}? (accept/decline): ")
                                process_response(idx, "doctor", resp.strip().lower())
                                # Ensure reminders are not sent multiple times for the same appointment
                                if __name__ == "__main__":
                                    reminded_appointments = set()

                                    def remind_appointments():
                                        now = datetime.datetime.now()
                                        for idx, appt in enumerate(appointments):
                                            if idx in reminded_appointments:
                                                continue
                                            if 0 <= (appt["datetime"] - now).days <= 1:
                                                subject = f"Appointment Reminder: {appt['datetime'].strftime('%Y-%m-%d %H:%M')}"
                                                patient_body = f"Dear {appt['patient_name']},\nThis is a reminder for your appointment with {appt['doctor_name']} on {appt['datetime']}."
                                                doctor_body = f"Dear {appt['doctor_name']},\nThis is a reminder for your appointment with {appt['patient_name']} on {appt['datetime']}."
                                                if appt["channel"] == "email":
                                                    send_email(appt["patient_email"], subject, patient_body)
                                                    send_email(appt["doctor_email"], subject, doctor_body)
                                                # Mark as reminded to avoid duplicate notifications
                                                reminded_appointments.add(idx)

                                    schedule.every(1).hours.do(remind_appointments)

                                    print("Scheduler started. Press Ctrl+C to exit.")
                                    while True:
                                        schedule.run_pending()
                                        time.sleep(1)




#  Problem: Clinics and private doctors often lose track of patient follow-ups.
#  Challenge: Develop a tool that automatically reminds both doctors and patients of appointments via SMS, WhatsApp, or other channels.
# Problem Statement:
# Clinics and doctors often miss patient follow-ups due to inefficient manual reminders. Build an automated tool to send timely appointment reminders to both doctors and patients via Email, SMS, or WhatsApp, and handle their responses to reduce missed appointments.
# Solution Statement:
# To address the problem of missed patient follow-ups due to inefficient manual reminders, the following automated solution is proposed:
#
# 1. Centralized Appointment Management:
#    - Store all appointment details (patient, doctor, contact info, date/time, preferred reminder channel) in a structured format.
#
# 2. Automated Multi-Channel Reminders:
#    - Automatically send timely reminders to both patients and doctors via their preferred channels (Email, SMS, WhatsApp).
#    - Integrate with email (SMTP) and messaging APIs (e.g., Twilio) for reliable delivery.
#
# 3. Scheduled Reminder System:
#    - Use a scheduling library to periodically check for upcoming appointments and trigger reminders at configurable intervals (e.g., 1 day before).
#
# 4. Response Handling:
#    - Allow recipients to accept or decline appointments, and record their responses for follow-up actions.
#
# 5. Duplicate Prevention:
#    - Track which appointments have already been reminded to avoid sending duplicate notifications.
#
# 6. Security and Configuration:
#    - Secure sensitive credentials (e.g., SMTP, API keys) using environment variables or configuration files.
#
# 7. Extensibility:
#    - Design the system to easily add new communication channels or integrate with clinic management systems.
#
# 8. Logging and Error Handling:
#    - Implement robust logging and error handling to monitor reminder delivery and troubleshoot issues.
#
# 9. Scalability:
#    - Use a database for persistent storage and support for larger volumes of appointments in production environments.
#
# This solution reduces missed appointments, improves communication, and streamlines follow-up processes for clinics and private doctors.



        
# Note: This is a simplified example. In a real-world application, you would want to handle exceptions,
# logging, and possibly use a task scheduler to run this script periodically.
# Also, ensure to secure your SMTP credentials and not hard-code them in the script.
# You can use environment variables or a configuration file for sensitive information.
# Additionally, consider using a library like `schedule` to run this script at regular intervals.
# For SMS/WhatsApp, you can use Twilio or similar services to send messages.
# For a production system, consider using a database to store appointments and a more robust
# scheduling system to handle reminders.
# This code is a basic example and should be adapted to fit your specific requirements and environment.
# Ensure to install necessary libraries if not already installed
# pip install schedule
# pip install twilio
# For email sending, you might need to install the `smtplib` library if not already available
# in your Python environment. This is usually included in the standard library.
# For SMS/WhatsApp, you can use Twilio or similar services to send messages.
# For a production system, consider using a database to store appointments and a more robust
# scheduling system to handle reminders.