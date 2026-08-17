import json

from services.llm_service import generate_response


EVALUATION_PROMPT = """
You are an experienced Senior Technical Interviewer.

Evaluate the candidate's answer to the interview question.

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer using these criteria:

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

Return ONLY a JSON object with exactly these fields:

{{
    "score": 8,
    "strengths": [
        "Example strength"
    ],
    "weaknesses": [
        "Example weakness"
    ],
    "suggestions": [
        "Example suggestion"
    ]
}}

The score MUST be an integer from 0 to 10.
The strengths, weaknesses, and suggestions MUST be arrays of strings.
Do not include markdown.
Do not include ```json.
"""


def evaluate_answer(question: str, answer: str):

    prompt = EVALUATION_PROMPT.format(
        question=question,
        answer=answer
    )

    try:

        response = generate_response(
            prompt=prompt,
            temperature=0.2,
            max_tokens=350,
            json_mode=True
        )

        print("EVALUATION RAW RESPONSE:")
        print(response)

        data = json.loads(response)

        score = int(data.get("score", 0))

        # Keep score between 0 and 10
        score = max(0, min(score, 10))

        return {
            "score": score,
            "strengths": data.get("strengths", []),
            "weaknesses": data.get("weaknesses", []),
            "suggestions": data.get("suggestions", []),
            "raw": response
        }

    except Exception as e:

        print("EVALUATION ERROR:", e)

        return {
            "score": 0,
            "strengths": [],
            "weaknesses": [
                f"Evaluation error: {str(e)}"
            ],
            "suggestions": [
                "Please try again."
            ]
        }