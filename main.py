import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from datetime import datetime, timedelta
import csv

# Load environment variables from a .env file
load_dotenv()

# Fetch email credentials from environment variables
SENDER_EMAIL = os.getenv("EMAIL_USER")
SENDER_PASSWORD = os.getenv("EMAIL_PASSWORD")

# SMTP server settings for Gmail
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Function to set up the SMTP connection
def setup_smtp():
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Start TLS encryption
        return server
    except Exception as e:
        print(f"Error setting up SMTP server: {e}")
        return None

# Function to send email reminder
def send_email(recipient_email, event_name, event_date, event_description):
    server = setup_smtp()
    if not server:
        return

    # Compose the email
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = f"Reminder: {event_name} is tomorrow!"

    # Email body content
    body = f"Hi,\n\nThis is a reminder that the following event is coming up tomorrow:\n\n" \
           f"Event: {event_name}\nDate: {event_date}\nDescription: {event_description}\n\n" \
           "Don't forget to prepare!\n\nBest regards,\nYour Reminder App"
    
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Login to the SMTP server
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        print(f"Reminder email sent to {recipient_email}")
    except smtplib.SMTPAuthenticationError:
        print("Error: Invalid email or app password. Please check your credentials.")
    except smtplib.SMTPException as e:
        print(f"SMTP Error: {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")
    finally:
        # Quit the server connection
        server.quit()

# Function to check upcoming events from the CSV
def check_upcoming_events(csv_filename):
    today = datetime.now()
    tomorrow = today + timedelta(days=1)  # Get tomorrow's date

    # Read events from the CSV
    with open(csv_filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        events = list(reader)

    # Loop through events to check for tomorrow's events
    for event in events:
        event_name = event[0]
        event_date = datetime.strptime(event[1], "%Y-%m-%d")
        event_description = event[2]
        recipient_email = event[3]  # Assume the recipient's email is in the 4th column

        # Check if the event is tomorrow
        if event_date.date() == tomorrow.date():
            print(f"Event {event_name} is tomorrow! Sending reminder...")
            send_email(recipient_email, event_name, event_date.strftime("%Y-%m-%d"), event_description)

# Main function
def main():
    csv_filename = "events.csv"  # Path to your CSV file
    check_upcoming_events(csv_filename)

if __name__ == "__main__":
    main()



