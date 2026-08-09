from services.llm_service import generate_response


SKILL_EXTRACTION_PROMPT = """
You are an expert technical recruiter.

Extract ONLY technical skills from the text below.

Rules:

1. Include:
- Programming Languages
- Frameworks
- Libraries
- Databases
- Cloud Platforms
- DevOps Tools
- AI/ML Technologies
- APIs
- Software Engineering Concepts

2. Return ONE skill per line.

3. Remove duplicates.

4. Do NOT include explanations.

Document:

{document}
"""


class SkillExtractionAgent:

    def extract_skills(self, document: list[str]):

        prompt = SKILL_EXTRACTION_PROMPT.format(
            document="\n".join(document)
        )

        response = generate_response(
            prompt=prompt,
            temperature=0.2,
            max_tokens=250
        )

        skills = []

        for line in response.splitlines():

            skill = line.strip()

            if (
                skill
                and skill not in skills
                and not skill.startswith("-")
            ):
                skills.append(skill)

        return skills


skill_extractor = SkillExtractionAgent()