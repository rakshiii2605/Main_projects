import streamlit as st
import pickle
from datetime import datetime, timedelta
from database import log_study
from emailer import send_email
from pdf_exporter import export_to_pdf

# Load model
with open("study_model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("\U0001F393 AI Study Plan Generator")

subjects = ["English", "Physics", "Maths", "EVS", "Python", "Data Structures"]
marks = []

st.header("Enter your marks:")
for subj in subjects:
    mark = st.number_input(f"{subj} marks:", 0, 100, step=1)
    marks.append(mark)

start_time = st.time_input("\U0001F4C5 Enter your study start time:")
end_time = st.time_input("\U0001F4C5 Enter your study end time:")
email = st.text_input("Enter your email to receive the plan:")

BREAK_DURATION = 10  # minutes

def calculate_available_minutes(start, end):
    start_dt = datetime.combine(datetime.today(), start)
    end_dt = datetime.combine(datetime.today(), end)
    if end_dt < start_dt:
        end_dt += timedelta(days=1)
    return int((end_dt - start_dt).total_seconds() // 60)

def get_plan(subjects, labels):
    plan = {}
    for subj, label in zip(subjects, labels):
        if label == "Weak":
            plan[subj] = 3
        elif label == "Moderate":
            plan[subj] = 2
        else:
            plan[subj] = 1
    return plan

def generate_timetable(plan, total_minutes, start_time):
    total_hours = sum(plan.values())
    total_breaks = max(total_hours - 1, 0)
    total_break_minutes = total_breaks * BREAK_DURATION
    available_study_minutes = total_minutes - total_break_minutes
    minutes_per_hour = available_study_minutes // total_hours if total_hours else 0

    timetable = []
    current_time = datetime.combine(datetime.today(), start_time)

    for idx, (subject, hours) in enumerate(plan.items()):
        duration = hours * minutes_per_hour
        end_time = current_time + timedelta(minutes=duration)
        timetable.append({
            "time_slot": f"{current_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}",
            "subject": subject
        })
        current_time = end_time

        if idx < len(plan) - 1:
            break_end = current_time + timedelta(minutes=BREAK_DURATION)
            timetable.append({
                "time_slot": f"{current_time.strftime('%I:%M %p')} - {break_end.strftime('%I:%M %p')}",
                "subject": "Break"
            })
            current_time = break_end

    return timetable

# Initialize session_state variables
if "plan_generated" not in st.session_state:
    st.session_state.plan_generated = False
if "plan" not in st.session_state:
    st.session_state.plan = {}
if "timetable" not in st.session_state:
    st.session_state.timetable = []
if "progress_state" not in st.session_state:
    st.session_state.progress_state = {}

if st.button("Generate Plan"):
    labels = model.predict([[m] for m in marks])
    plan = get_plan(subjects, labels)
    total_minutes = calculate_available_minutes(start_time, end_time)
    timetable = generate_timetable(plan, total_minutes, start_time)

    for subject, hours in plan.items():
        log_study(subject, hours)

    st.session_state.plan_generated = True
    st.session_state.plan = plan
    st.session_state.timetable = timetable
    st.session_state.progress_state = {}

if st.session_state.plan_generated:
    plan = st.session_state.plan
    timetable = st.session_state.timetable

    st.subheader("\U0001F4D8 Your Personalized Study Plan:")
    for subject, hours in plan.items():
        st.write(f"**{subject}**: {hours} hours/day")
        st.progress(min(hours / 3, 1.0))

    st.subheader("\U0001F552 Study Time Table with Breaks:")

    completed_sessions = {subj: 0 for subj in subjects}
    total_sessions = {subj: 0 for subj in subjects}

    for i, slot in enumerate(timetable):
        if slot["subject"] == "Break":
            st.write(f"⏸️ **Break:** {slot['time_slot']}")
        else:
            total_sessions[slot["subject"]] += 1
            key = f"chk_{i}"
            if key not in st.session_state.progress_state:
                st.session_state.progress_state[key] = False

            completed = st.checkbox(f"{slot['time_slot']} : {slot['subject']}",
                                    value=st.session_state.progress_state[key],
                                    key=key)
            st.session_state.progress_state[key] = completed

            if completed:
                completed_sessions[slot["subject"]] += 1

    st.subheader("\U0001F4CA Your Study Progress:")
    overall_total = sum(total_sessions.values())
    overall_completed = sum(completed_sessions.values())

    for subj in subjects:
        total = total_sessions[subj]
        completed = completed_sessions[subj]
        if total > 0:
            percent = int((completed / total) * 100)
            st.write(f"**{subj}**: {percent}% complete ({completed} of {total} sessions)")
        else:
            st.write(f"**{subj}**: No sessions scheduled")

    if overall_total > 0:
        overall_percent = int((overall_completed / overall_total) * 100)
        st.write(f"### Overall Progress: {overall_percent}% complete")

    if email:
        if st.button("Send Email"):
            send_email(plan, timetable, st.session_state.progress_state, subjects, email)
            st.success("\U0001F4E7 Email sent!")

    if st.button("\U0001F4C4 Download as PDF"):
        pdf_data = export_to_pdf(plan, timetable, st.session_state.progress_state, subjects)
        st.download_button(
            label="Download PDF",
            data=pdf_data,
            file_name="study_plan.pdf",
            mime="application/pdf"
        )


