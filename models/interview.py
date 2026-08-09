from dataclasses import dataclass, field
from typing import List


@dataclass
class InterviewSession:

    # Resume Information
    resume_skills: List[str] = field(default_factory=list)

    # Job Description Information
    job_skills: List[str] = field(default_factory=list)

    # Planned Interview Topics
    interview_plan: List[str] = field(default_factory=list)

    # Completed Topics
    covered_topics: List[str] = field(default_factory=list)

    # Interview Questions
    questions: List[str] = field(default_factory=list)

    # Candidate Answers
    answers: List[str] = field(default_factory=list)

    # AI Evaluations
    feedback: List[dict] = field(default_factory=list)

    # Current Question
    current_question: str = ""

    # Current Topic
    current_topic: str = ""

    # Progress
    current_question_number: int = 0
    total_questions: int = 5

    # Difficulty
    current_difficulty: str = "Easy"

    # Status
    is_started: bool = False
    is_completed: bool = False

    # Final Score
    overall_score: float = 0.0

    # Summary
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)