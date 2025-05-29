import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(plan, timetable, progress_state, subjects, to_email):
    message = MIMEMultipart("alternative")
    message["Subject"] = "📘 Your Daily Study Plan"
    message["From"] = "studywithrobot@gmail.com"
    message["To"] = to_email

    text = "📘 Your Study Plan:\n\n"
    for subject, hours in plan.items():
        text += f"{subject}: {hours} hours/day\n"

    text += "\n🕒 Study Time Table with Breaks:\n"
    for i, slot in enumerate(timetable):
        if slot["subject"] == "Break":
            text += f"\n⏸️ Break: {slot['time_slot']}\n"
        else:
            key = f"chk_{i}"
            done = progress_state.get(key, False)
            check = "✅" if done else "❌"
            text += f"{slot['time_slot']} : {slot['subject']} {check}\n"

    text += "\n📊 Your Progress:\n"
    subject_sessions = {subj: {"done": 0, "total": 0} for subj in subjects}
    for i, slot in enumerate(timetable):
        if slot["subject"] != "Break":
            subj = slot["subject"]
            subject_sessions[subj]["total"] += 1
            if progress_state.get(f"chk_{i}", False):
                subject_sessions[subj]["done"] += 1

    for subj in subjects:
        done = subject_sessions[subj]["done"]
        total = subject_sessions[subj]["total"]
        if total > 0:
            percent = int((done / total) * 100)
            text += f"{subj}: {percent}% complete ({done}/{total})\n"
        else:
            text += f"{subj}: No sessions scheduled\n"

    part = MIMEText(text, "plain")
    message.attach(part)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login("studywithrobot@gmail.com", "miteyuqfvjytpjaw")
        server.send_message(message)

