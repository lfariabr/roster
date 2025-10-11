import smtplib
import ssl
from email.message import EmailMessage
import streamlit as st

def send_email_with_attachment(to_email, subject, body, csv_bytes, filename):
    """Send an email using Gmail SMTP + App Password."""
    smtp_server = "smtp.gmail.com"
    port = 465  # SSL port
    sender_email = "excelbmpilot@gmail.com"
    app_password = st.secrets["gmail"]["app_password"]

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    # Attach the CSV file
    msg.add_attachment(csv_bytes, maintype="text", subtype="csv", filename=filename)

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"❌ Email sending failed: {e}")
        return False
