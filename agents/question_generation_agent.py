from services.llm_service import generate_response

from rag.retriever import retrieve_combined_context


QUESTION_GENERATION_PROMPT = """
You are a Senior Technical Interviewer.

Candidate Resume + Job Context:
{context}

Current Interview Topic:
{topic}

Difficulty:
{difficulty}

Previous Questions:
{previous_questions}

Previous Answers:
{previous_answers}

Previous Evaluation Scores:
{scores}

Covered Topics:
{covered_topics}

Question Number:
{question_number}

Instructions:

1. Ask ONLY ONE interview question.

2. The question MUST focus on the current topic.

3. Do NOT repeat previous questions.

4. Match the requested difficulty.

5. Personalize the question using the candidate's resume whenever possible.

6. If this is a later question, build naturally on earlier discussion without requiring the candidate to repeat themselves.

7. Prefer scenario-based and practical questions over textbook definitions.

Difficulty Guide:

Easy:
- Definitions
- Basic concepts
- Resume walkthrough

Medium:
- Design decisions
- Debugging
- APIs
- Best practices
- Trade-offs

Hard:
- Architecture
- Performance
- Scalability
- Edge cases
- Production systems

Return ONLY the interview question.
"""


def generate_interview_question(
    user_id,
    topic,
    question_number,
    previous_questions,
    difficulty="Easy",
    previous_answers=None,
    previous_feedback=None,
    covered_topics=None,
):

    if previous_answers is None:
        previous_answers = []

    if previous_feedback is None:
        previous_feedback = []

    if covered_topics is None:
        covered_topics = []

    context = retrieve_combined_context(user_id)


    scores = [
        str(item.get("score", ""))
        for item in previous_feedback
    ]

    prompt = QUESTION_GENERATION_PROMPT.format(
        context="\n".join(context),
        topic=topic,
        difficulty=difficulty,
        previous_questions="\n".join(previous_questions) or "None",
        previous_answers="\n".join(previous_answers) or "None",
        scores="\n".join(scores) or "None",
        covered_topics="\n".join(covered_topics) or "None",
        question_number=question_number,
    )

    response = generate_response(
        prompt=prompt,
        temperature=0.4,
        max_tokens=250,
    )

    return response.strip()