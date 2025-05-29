# 📘 AI-Based Personalized Study Plan Generator

An intelligent web app that generates a personalized daily study timetable based on your subject performance and available time. Built using Python, Streamlit, and Machine Learning, it also allows PDF export and email delivery of your plan.

---

## 📌 Features

- 🧠 AI-based subject strength detection (Weak/Moderate/Strong)
- 📅 Personalized study timetable generator
- ⏱ Custom input for available daily study time
- 💌 Email the plan directly to your inbox
- 📄 Download study plan as a styled PDF
- ✅ Progress logging with SQLite
- 🎨 Stylish interface with pastel themes and logo branding

---

## 🛠️ Tech Stack

| Component          | Tools / Libraries                        |
|-------------------|-------------------------------------------|
| Frontend           | Streamlit                                 |
| Backend            | Python                                    |
| ML Model           | Scikit-learn, Pandas                      |
| PDF Export         | FPDF                                      |
| Email Integration  | smtplib, SSL                              |
| Database           | SQLite3                                   |

---

## 📂 Folder Structure
study-plan-ai/
├── app.py # Main Streamlit app
├── planner.py # Logic to calculate study plan
├── database.py # Logs study data in SQLite
├── emailer.py # Sends email with study plan
├── pdf_exporter.py # Exports plan to styled PDF
├── study_model.pkl # Trained ML model
├── student_data.csv # Sample dataset
├── README.md # Project documentation
└── assets/ # Logo and custom styles (optional)

---

## 🛠️ Technologies Used

- Python 3
- Streamlit
- Pandas
- SQLite3
- scikit-learn
- FPDF
- smtplib/email

