from models.interview import InterviewSession

from agents.interview_planner import planner
from agents.skill_extraction_agent import skill_extractor
from agents.question_generation_agent import generate_interview_question
from agents.evaluation_agent import evaluate_answer
from database.database import get_previous_questions
from rag.retriever import (
    retrieve_resume_context,
    retrieve_job_context,
)



class InterviewAgent:

    def __init__(self):
        self.session = InterviewSession()
        self.user_id = None

    def start_interview(self, user_id):

        self.user_id = user_id

        self.session = InterviewSession()

        self.session.is_started = True
        self.session.is_completed = False

        self.session.current_question_number = 1
        self.session.current_difficulty = "Easy"

        resume_context = retrieve_resume_context(self.user_id)
        job_context = retrieve_job_context(self.user_id)

        self.session.resume_skills = skill_extractor.extract_skills(resume_context)
        self.session.job_skills = skill_extractor.extract_skills(job_context)

        self.session.interview_plan = planner.create_plan(
            self.session.resume_skills,
            self.session.job_skills
    )

        self.session.current_topic = self._get_current_topic()
        previous_questions = get_previous_questions(self.user_id)

        self.session.current_question = generate_interview_question(
            user_id=self.user_id,
            topic=self.session.current_topic,
            question_number=self.session.current_question_number,
            difficulty=self.session.current_difficulty,
            previous_questions=previous_questions,
            previous_answers=self.session.answers,
            previous_feedback=self.session.feedback,
            covered_topics=self.session.covered_topics,
    )
        
    def submit_answer(self, answer):
        """
        Evaluates candidate answer.
        """

        self.session.answers.append(answer)

        evaluation = evaluate_answer(
            self.session.current_question,
            answer,
        )

        self.session.feedback.append(evaluation)

        self.session.questions.append(
            self.session.current_question
        )

        self.session.covered_topics.append(
            self.session.current_topic
        )

        # Interview Finished
        if self.session.current_question_number >= self.session.total_questions:

            self.session.is_completed = True
            self.session.is_started = False

            scores = [
                item.get("score", 0)
                for item in self.session.feedback
            ]

            if scores:
                self.session.overall_score = round(
                    sum(scores) / len(scores),
                    2,
                )

            # Aggregate strengths
            strengths = []
            weaknesses = []
            recommendations = []

            for feedback in self.session.feedback:

                strengths.extend(
                    feedback.get("strengths", [])
                )

                weaknesses.extend(
                    feedback.get("weaknesses", [])
                )

                recommendations.extend(
                    feedback.get("suggestions", [])
                )

            # Remove duplicates while preserving order
            self.session.strengths = list(dict.fromkeys(strengths))
            self.session.weaknesses = list(dict.fromkeys(weaknesses))
            self.session.recommendations = list(dict.fromkeys(recommendations))

            #save_interview(self.session)

        return evaluation

    def move_to_next_question(self):
        """
        Generates the next interview question.
        """

        if self.session.is_completed:
            return

        self.session.current_question_number += 1

        # Progressive Difficulty
        if self.session.current_question_number <= 2:
            self.session.current_difficulty = "Easy"

        elif self.session.current_question_number <= 4:
            self.session.current_difficulty = "Medium"

        else:
            self.session.current_difficulty = "Hard"

        self.session.current_topic = self._get_current_topic()

        self.session.current_question = generate_interview_question(
            user_id=self.user_id,
            topic=self.session.current_topic,
            question_number=self.session.current_question_number,
            difficulty=self.session.current_difficulty,
            previous_questions=self.session.questions,
            previous_answers=self.session.answers,
            previous_feedback=self.session.feedback,
            covered_topics=self.session.covered_topics,
        )

    def _get_current_topic(self):
        """
        Returns the interview topic for the current question.
        """

        index = self.session.current_question_number - 1

        if index < len(self.session.interview_plan):
            return self.session.interview_plan[index]

        return "General Technical Knowledge"


interview_agent = InterviewAgent()