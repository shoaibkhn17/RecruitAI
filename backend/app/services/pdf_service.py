import os

os.makedirs(
    "reports",
    exist_ok=True
)

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


def generate_report(
    file_path,
    candidate_email,
    resume_score,
    interview_score,
    recommendation
):

    doc = SimpleDocTemplate(file_path)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "RECRUITAI - AI INTERVIEW EVALUATION REPORT",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    report_text = f"""
    <b>INTERVIEW STATUS</b><br/><br/>

    ✓ Interview Successfully Completed<br/><br/>

    Thank you for participating in the RecruitAI AI-Powered Recruitment Process.<br/><br/>

    ====================================================<br/><br/>

    <b>CANDIDATE INFORMATION</b><br/><br/>

    Candidate Email: {candidate_email}<br/>
    Application Status: Completed<br/><br/>

    ====================================================<br/><br/>

    <b>RESUME ANALYSIS</b><br/><br/>

    Resume Match Score: {resume_score}%<br/><br/>

    ====================================================<br/><br/>

    <b>AI INTERVIEW ANALYSIS</b><br/><br/>

    Interview Score: {interview_score}%<br/><br/>

    ====================================================<br/><br/>

    <b>FINAL RECOMMENDATION</b><br/><br/>

    Decision: {recommendation}<br/><br/>

    ====================================================<br/><br/>

    <b>RECRUITAI TECHNOLOGY STACK</b><br/><br/>

    • AI Resume Screening Engine<br/>
    • Speech-to-Text Processing<br/>
    • AI Interview Evaluation System<br/>
    • Candidate Scoring Engine<br/>
    • MongoDB Analytics Database<br/><br/>

    ====================================================<br/><br/>

    <b>THANK YOU</b><br/><br/>

    Thank you for completing the RecruitAI AI-Powered Interview Assessment.<br/><br/>

    RecruitAI - Smart Hiring Through Artificial Intelligence
    """

    content.append(
        Paragraph(
            report_text,
            styles["Normal"]
        )
    )

    doc.build(content)

    return file_path