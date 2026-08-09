from io import BytesIO

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate


def generate_pdf(report: str) -> BytesIO:
    """
    Convert markdown/text interview report into a PDF.
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    for line in report.split("\n"):

        line = line.strip()

        if not line:
            story.append(Paragraph("<br/>", styles["Normal"]))
            continue

        if line.startswith("# "):
            story.append(
                Paragraph(
                    f"<b>{line.replace('# ', '')}</b>",
                    styles["Heading1"]
                )
            )

        elif line.startswith("## "):
            story.append(
                Paragraph(
                    f"<b>{line.replace('## ', '')}</b>",
                    styles["Heading2"]
                )
            )

        elif line.startswith("### "):
            story.append(
                Paragraph(
                    f"<b>{line.replace('### ', '')}</b>",
                    styles["Heading3"]
                )
            )

        else:
            story.append(
                Paragraph(line, styles["BodyText"])
            )

    doc.build(story)

    buffer.seek(0)

    return buffer