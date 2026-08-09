from agents.report_generation_agent import report_generator


def generate_interview_report(session) -> str:
    """
    Generate the final interview report.
    """

    if session is None:
        raise ValueError("Interview session not found.")

    if not session.is_completed:
        raise ValueError(
            "Interview must be completed before generating a report."
        )

    return report_generator.generate_report(session)