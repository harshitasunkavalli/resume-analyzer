from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(filename, score, match_score, skills, jobs, feedback):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("AI Resume Analysis Report", styles['Title']))
    content.append(Spacer(1, 20))

    content.append(Paragraph(f"<b>ATS Score:</b> {score}%", styles['Normal']))
    content.append(Spacer(1,10))

    content.append(Paragraph(f"<b>Match Score:</b> {match_score}%", styles['Normal']))
    content.append(Spacer(1,10))

    content.append(Paragraph("<b>Skills:</b>", styles['Heading2']))
    content.append(Paragraph(", ".join(skills) or "None", styles['Normal']))
    content.append(Spacer(1,10))

    content.append(Paragraph("<b>Recommended Jobs:</b>", styles['Heading2']))
    content.append(Paragraph(", ".join(jobs) or "None", styles['Normal']))
    content.append(Spacer(1,10))

    content.append(Paragraph("<b>Feedback:</b>", styles['Heading2']))

    for f in feedback:
        content.append(Paragraph(f"- {f}", styles['Normal']))

    doc.build(content)