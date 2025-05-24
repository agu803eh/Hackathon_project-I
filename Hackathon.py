#pip install schedule
# pip install twilio
import datetime
import smtplib
from email.mime.text import MIMEText
import schedule
import time
from twilio.rest import Client
import os
import logging

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
                                        # Extensibility: Add new communication channels via a unified interface

                                        class Channel:
                                            def send(self, to, subject, body):
                                                raise NotImplementedError

                                        class EmailChannel(Channel):
                                            def send(self, to, subject, body):
                                                send_email(to, subject, body)

                                        # Example placeholder for SMS channel (implement with Twilio or similar)
                                        class SMSChannel(Channel):
                                            def send(self, to, subject, body):
                                                # Integrate with SMS API here
                                                print(f"SMS sent to {to}: {body}")

                                        # Example placeholder for WhatsApp channel (implement with Twilio or similar)
                                        class WhatsAppChannel(Channel):
                                            def send(self, to, subject, body):
                                                # Integrate with WhatsApp API here
                                                print(f"WhatsApp sent to {to}: {body}")

                                        # Channel registry for easy extension
                                        CHANNELS = {
                                            "email": EmailChannel(),
                                            "sms": SMSChannel(),
                                            "whatsapp": WhatsAppChannel(),
                                        }

                                        def send_reminder(channel_name, to, subject, body):
                                            channel = CHANNELS.get(channel_name)
                                            if channel:
                                                channel.send(to, subject, body)
                                            else:
                                                print(f"Channel '{channel_name}' not supported.")

                                        # Example usage in reminder logic:
                                        # send_reminder(appt["channel"], appt["patient_contact"], subject, patient_body)

                                        # Integration point for clinic management systems:
                                        # You can define functions to import/export appointments from/to external systems (e.g., via API, CSV, database)
                                        def import_appointments_from_clinic_system():
                                            # Implement integration logic here
                                            pass

                                        def export_appointments_to_clinic_system():
                                            # Implement integration logic here
                                            pass

                                            # Twilio integration for SMS and WhatsApp

                                            # Set your Twilio credentials as environment variables for security
                                            TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "your_account_sid")
                                            TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "your_auth_token")
                                            TWILIO_SMS_FROM = os.getenv("TWILIO_SMS_FROM", "+1234567890")  # Your Twilio SMS number
                                            TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM", "whatsapp:+1234567890")  # Your Twilio WhatsApp number

                                            twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

                                            class SMSChannel(Channel):
                                                def send(self, to, subject, body):
                                                    try:
                                                        twilio_client.messages.create(
                                                            body=body,
                                                            from_=TWILIO_SMS_FROM,
                                                            to=to
                                                        )
                                                        print(f"SMS sent to {to}: {body}")
                                                    except Exception as e:
                                                        print(f"Failed to send SMS to {to}: {e}")

                                            class WhatsAppChannel(Channel):
                                                def send(self, to, subject, body):
                                                    try:
                                                        # WhatsApp numbers must be in the format 'whatsapp:+1234567890'
                                                        if not to.startswith("whatsapp:"):
                                                            to = f"whatsapp:{to}"
                                                        twilio_client.messages.create(
                                                            body=body,
                                                            from_=TWILIO_WHATSAPP_FROM,
                                                            to=to
                                                        )
                                                        print(f"WhatsApp sent to {to}: {body}")
                                                    except Exception as e:
                                                        print(f"Failed to send WhatsApp to {to}: {e}")

                                            # Update the CHANNELS registry to use the new Twilio-enabled channels
                                            CHANNELS["sms"] = SMSChannel()
                                            CHANNELS["whatsapp"] = WhatsAppChannel()
                                            # Example: Send SMS reminder to Dr. Smith
                                            sms_subject = "Appointment Reminder: 2025-05-26 10:00"
                                            sms_body = "Dear Dr. Smith,\nThis is a reminder for your appointment with John Wick on 2025-05-26 10:00."
                                            send_reminder("sms", "+2349087654321", sms_subject, sms_body)

                                            # Example: Send WhatsApp reminder to Agu Miracle
                                            wa_subject = "Appointment Reminder: 2025-05-25 14:30"
                                            wa_body = "Dear Agu Miracle,\nThis is a reminder for your appointment with Dr. Strange on 2025-05-25 14:30."
                                            send_reminder("whatsapp", "+2348134814891", wa_subject, wa_body)
                                            # Configure logging
                                            logging.basicConfig(
                                                filename="reminder_system.log",
                                                level=logging.INFO,
                                                format="%(asctime)s [%(levelname)s] %(message)s"
                                            )

                                            def log_and_print(level, message):
                                                print(message)
                                                if level == "info":
                                                    logging.info(message)
                                                elif level == "warning":
                                                    logging.warning(message)
                                                elif level == "error":
                                                    logging.error(message)
                                                else:
                                                    logging.debug(message)

                                            # Example: Wrap send_reminder with logging and error handling
                                            def send_reminder_with_logging(channel_name, to, subject, body):
                                                try:
                                                    send_reminder(channel_name, to, subject, body)
                                                    log_and_print("info", f"Reminder sent via {channel_name} to {to}: {subject}")
                                                except Exception as e:
                                                    log_and_print("error", f"Failed to send reminder via {channel_name} to {to}: {e}")

