import smtplib
import streamlit as st
from email.message import EmailMessage
import requests


def send_email(to, subject, body):
    r = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        headers={
            "api-key": st.secrets["BREVO_API_KEY"],
            "content-type": "application/json",
        },
        json={
            "sender": {"name": "Snap Class", "email": st.secrets["SENDER_EMAIL"]},
            "to": [{"email": to}],
            "subject": subject,
            "textContent": body,
        },
        timeout=30,
    )
    if r.status_code >= 400:
        raise Exception(f"Brevo {r.status_code}: {r.text}")


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
            sent += 1
        except Exception as e:
            failed += 1
            errors.append(f"{s['name']}:{type(e).__name__}: {e}")
    return sent, failed, errors
