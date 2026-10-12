import smtplib
import streamlit as st
from email.message import EmailMessage


def send_email(to, subject, body):
    msg = EmailMessage()
    msg["From"] = st.secrets["EMAIL_USER"]
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as s:
        s.ehlo()
        s.starttls()
        s.ehlo()
        s.login(st.secrets["EMAIL_USER"], st.secrets["EMAIL_APP_PASSWORD"])
        s.send_message(msg)


def send_sms(to, body):
    from twilio.rest import Client
    client = Client(st.secrets["TWILIO_SID"], st.secrets["TWILIO_TOKEN"])
    client.messages.create(body=body, from_=st.secrets["TWILIO_FROM"], to=to)


def notify_absentees(absent_students, subject_name):
    sent, failed, errors = 0, 0, []
    for s in absent_students:
        text = f"{s['name']} was marked absent in {subject_name} today."
        try:
            if s.get("email"):
                send_email(s["email"], "Absence notice", text)
            if s.get("parent_phone"):
                send_sms(s["parent_phone"], text)
            sent += 1
        except Exception as e:
            failed += 1
            errors.append(f"{s['name']}:{type(e).__name__}: {e}")
    return sent, failed, errors
