from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def export_pdf(filename, query, summary):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = [
        Paragraph(f"<b>Query:</b> {query}", styles["Normal"]),
        Paragraph("<br/>", styles["Normal"]),
        Paragraph("<b>Summary:</b>", styles["Heading2"]),
        Paragraph(summary, styles["Normal"])
    ]

    doc.build(content)
