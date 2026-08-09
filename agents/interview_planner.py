from services.llm_service import generate_response


PLANNER_PROMPT = """
You are a Senior Technical Interviewer.

Resume Skills:
{resume_skills}

Job Skills:
{job_skills}

Create a technical interview plan.

Rules:

1. Prioritize skills that appear in BOTH lists.

2. Then include important skills from the job description that are missing from the resume.

3. Avoid duplicate topics.

4. Order the interview from easy to hard.

5. Return EXACTLY 5 topics.

6. One topic per line.

Example:

Python
FastAPI
Docker
AWS
System Design

Return ONLY the topics.
"""


class InterviewPlanner:

    def create_plan(
        self,
        resume_skills: list[str],
        job_skills: list[str]
    ):

        prompt = PLANNER_PROMPT.format(
            resume_skills="\n".join(resume_skills),
            job_skills="\n".join(job_skills)
        )

        response = generate_response(
            prompt=prompt,
            temperature=0.2,
            max_tokens=150
        )

        topics = []

        for line in response.splitlines():

            topic = line.strip()

            if (
                topic
                and topic not in topics
                and not topic.startswith("-")
            ):
                topics.append(topic)

        topics = topics[:5]

        while len(topics) < 5:
            topics.append("General Technical Knowledge")

        return topics


planner = InterviewPlanner()