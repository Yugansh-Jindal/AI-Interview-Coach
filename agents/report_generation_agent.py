from services.llm_service import generate_response


REPORT_PROMPT = """
You are an expert Technical Interview Coach.

Generate a professional interview report.

Candidate Interview Data:

{interview_data}

Generate the report using the following sections:

# Overall Performance

Give a concise summary of the interview.

# Technical Strengths

Summarize the candidate's strongest technical skills.

# Areas for Improvement

Identify recurring weaknesses.

# Question-by-Question Analysis

For each question provide:

Question:
Candidate Answer Summary:
Score:
Feedback:

# Recommendations

Provide practical recommendations for improving interview performance.

# Final Verdict

Choose ONE:

Excellent Candidate
Strong Candidate
Good Candidate
Needs Improvement

Keep the report professional and concise.
"""


class ReportGenerationAgent:

    def generate_report(self, session):

        report = []

        report.append(f"Overall Score: {session.overall_score}/10")
        report.append("")

        for index in range(len(session.questions)):

            question = session.questions[index]

            answer = (
                session.answers[index]
                if index < len(session.answers)
                else ""
            )

            feedback = (
                session.feedback[index]
                if index < len(session.feedback)
                else {}
            )

            score = feedback.get("score", 0)

            strengths = ", ".join(
                feedback.get("strengths", [])
            )

            weaknesses = ", ".join(
                feedback.get("weaknesses", [])
            )

            suggestions = ", ".join(
                feedback.get("suggestions", [])
            )

            report.extend([
                f"Question {index + 1}",
                f"Topic: {session.covered_topics[index] if index < len(session.covered_topics) else 'N/A'}",
                f"Question: {question}",
                f"Answer: {answer}",
                f"Score: {score}",
                f"Strengths: {strengths}",
                f"Weaknesses: {weaknesses}",
                f"Suggestions: {suggestions}",
                ""
            ])

        report.append("Overall Strengths")
        report.extend(session.strengths)

        report.append("")
        report.append("Overall Weaknesses")
        report.extend(session.weaknesses)

        report.append("")
        report.append("Recommendations")
        report.extend(session.recommendations)

        prompt = REPORT_PROMPT.format(
            interview_data="\n".join(report)
        )

        return generate_response(
            prompt=prompt,
            temperature=0.3,
            max_tokens=1200,
        )


report_generator = ReportGenerationAgent()