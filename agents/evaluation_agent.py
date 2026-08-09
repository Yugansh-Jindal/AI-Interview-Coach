import json

from services.llm_service import generate_response


EVALUATION_PROMPT = """
You are an experienced Senior Technical Interviewer.

Evaluate the candidate's answer.

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer on the following criteria:

1. Technical Accuracy
2. Completeness
3. Clarity
4. Communication
5. Best Practices

Scoring Rules:
- Return a SINGLE INTEGER score between 0 and 10.
- 0 = Completely incorrect.
- 5 = Average answer with noticeable gaps.
- 8 = Good answer with only minor issues.
- 10 = Excellent, interview-ready answer.

Return ONLY valid JSON.

Example:

{{
    "score": 8,
    "strengths": [
        "...",
        "..."
    ],
    "weaknesses": [
        "...",
        "..."
    ],
    "suggestions": [
        "...",
        "..."
    ]
}}
"""


def evaluate_answer(question: str, answer: str):

    prompt = EVALUATION_PROMPT.format(
        question=question,
        answer=answer
    )

    response = generate_response(
        prompt=prompt,
        temperature=0.2,
        max_tokens=350
    )

    try:

        start = response.find("{")
        end = response.rfind("}") + 1

        data = json.loads(response[start:end])

        score = int(data.get("score", 0))

        # Clamp score between 0 and 10
        score = max(0, min(score, 10))

        return {
            "score": score,
            "strengths": data.get("strengths", []),
            "weaknesses": data.get("weaknesses", []),
            "suggestions": data.get("suggestions", []),
            "raw": response
        }

    except Exception:

        return {
            "score": 0,
            "strengths": [],
            "weaknesses": ["Unable to evaluate answer."],
            "suggestions": ["Try answering with more technical detail."],
            "raw": response
        }