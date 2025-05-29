from fpdf import FPDF
from io import BytesIO
from datetime import datetime

class PDF(FPDF):
    def header(self):
        # Pastel green background
        self.set_fill_color(135, 206, 250)  # pastel green
        self.rect(0, 0, 210, 297, 'F')      # fill A4 page

        # Logo and date
        self.set_font("Times", "B", 14)
        self.set_text_color(0, 0, 0)
        self.set_xy(10, 10)
        self.cell(100, 10, "StudyWithAI :)", ln=False)

        self.set_font("Times", "", 10)
        self.set_xy(110, 10)
        today = datetime.now().strftime("%d-%m-%Y")
        self.cell(90, 10, f"Date: {today}", ln=False, align="R")

        # Title
        self.set_font("Times", "B", 20)
        self.set_xy(10, 30)
        self.cell(190, 15, "YOUR PERSONALIZED STUDY PLAN <3", ln=True, align="C")
        self.ln(10)

    def section_title(self, title):
        self.set_font("Arial", "B", 14)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, title, ln=True)
        self.ln(2)

    def write_line(self, text, bold=False):
        self.set_font("Helvetica", "B" if bold else "", 12)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 8, text)
        self.ln(1)

def export_to_pdf(plan_dict, timetable=None, progress_state=None, subjects=None):
    pdf = PDF()
    pdf.add_page()

    # Section 1: Study Plan
    pdf.section_title("Study Plan:)")
    for subject, hours in plan_dict.items():
        pdf.write_line(f"{subject}: {hours} hours/day", bold=True)

    # Section 2: Timetable
    if timetable:
        pdf.section_title(" Study Timetable with Breaks")
        for i, slot in enumerate(timetable):
            time_slot = slot["time_slot"]
            subject = slot["subject"]
            if subject == "Break":
                pdf.write_line(f" Break: {time_slot}")
            else:
                key = f"chk_{i}"
                status = "completed" if progress_state and progress_state.get(key) else "In progress"
                pdf.write_line(f"{time_slot} - {subject} {status}")

    # Section 3: Progress Summary
    if timetable and progress_state and subjects:
        pdf.section_title("Progress Summary")
        total_sessions = {subj: 0 for subj in subjects}
        completed_sessions = {subj: 0 for subj in subjects}
        for i, slot in enumerate(timetable):
            subj = slot["subject"]
            if subj != "Break":
                total_sessions[subj] += 1
                if progress_state.get(f"chk_{i}", False):
                    completed_sessions[subj] += 1

        for subj in subjects:
            total = total_sessions[subj]
            done = completed_sessions[subj]
            if total > 0:
                percent = int((done / total) * 100)
                pdf.write_line(f"{subj}: {percent}% complete ({done}/{total})")
            else:
                pdf.write_line(f"{subj}: No sessions scheduled")

        # Overall progress
        overall_total = sum(total_sessions.values())
        overall_done = sum(completed_sessions.values())
        if overall_total > 0:
            percent = int((overall_done / overall_total) * 100)
            pdf.write_line(f"\nOverall Progress: {percent}% complete")

    # Return BytesIO PDF buffer
    pdf_output = pdf.output(dest="S").encode("latin-1")
    return BytesIO(pdf_output)
