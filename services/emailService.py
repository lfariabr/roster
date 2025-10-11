import smtplib
import ssl
from email.message import EmailMessage
import streamlit as st
import re

def _html_to_text(html: str) -> str:
    """Very simple fallback conversion so email has a text part."""
    text = re.sub(r"<br\s*/?>", "\n", html, flags=re.I)
    text = re.sub(r"</p\s*>", "\n\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)  # strip tags
    return re.sub(r"\n{3,}", "\n\n", text).strip()

def send_email_with_attachment(
    to_email: str,
    subject: str,
    body_html: str,
    csv_bytes: bytes,
    filename: str,
    cc_email: str | None = None,
):
    """Send an email using Gmail SMTP + App Password, with optional CC and HTML body."""
    smtp_server = "smtp.gmail.com"
    port = 465  # SSL
    sender_email = "excelbmpilot@gmail.com"
    app_password = st.secrets["gmail"]["app_password"]

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    if cc_email:
        msg["Cc"] = cc_email

    # Add plain-text and HTML alternatives
    msg.set_content(_html_to_text(body_html))
    msg.add_alternative(body_html, subtype="html")

    # Attach CSV
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
