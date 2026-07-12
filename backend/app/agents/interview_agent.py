"""RecruitIQ Interview Intelligence Agent."""

from typing import Dict, Any, List
from loguru import logger

from app.agents.base_agent import BaseAgent


class InterviewAgent(BaseAgent):
    """Job-aware interview question generation agent."""

    def __init__(self):
        super().__init__(
            name="InterviewAgent",
            version="2.0.0",
        )

    async def execute(
        self,
        input_data: Dict[str, Any],
    ) -> Dict[str, Any]:

        candidate_skills = input_data.get(
            "candidate_skills",
            [],
        )

        job_requirements = input_data.get(
            "job_requirements",
            [],
        )

        experience_years = input_data.get(
            "experience_years",
            0,
        )

        difficulty = input_data.get(
            "difficulty",
            "medium",
        )

        num_questions = input_data.get(
            "num_questions",
            5,
        )

        logger.info(
            f"{self.name}: Generating intelligent interview questions"
        )

        questions = self._generate_questions(
            candidate_skills=candidate_skills,
            job_requirements=job_requirements,
            experience_years=experience_years,
            difficulty=difficulty,
            num_questions=num_questions,
        )

        return {
            "difficulty": difficulty,
            "num_questions": len(
                questions
            ),
            "questions": questions,
        }

    def _generate_questions(
        self,
        candidate_skills: List[str],
        job_requirements: List[str],
        experience_years: float,
        difficulty: str,
        num_questions: int,
    ) -> List[Dict[str, Any]]:

        questions = []

        candidate_skills_lower = [
            str(skill).lower()
            for skill in candidate_skills
        ]

        skill_gaps = []

        for requirement in (
            job_requirements
        ):
            if (
                str(requirement).lower()
                not in candidate_skills_lower
            ):
                skill_gaps.append(
                    requirement
                )

        # --------------------------------------------------
        # 1. Ask gap-based questions first
        # --------------------------------------------------

        for skill in skill_gaps:

            questions.append(
                {
                    "question":
                    f"Your resume does not show experience with {skill}. How would you learn and apply it in a production environment?",
                    "topic": skill,
                    "difficulty":
                    difficulty,
                    "suggested_answer":
                    f"Candidate should demonstrate learning strategy and practical application of {skill}.",
                }
            )

        # --------------------------------------------------
        # 2. Ask questions on matched skills
        # --------------------------------------------------

        for skill in candidate_skills[
            :3
        ]:

            questions.append(
                {
                    "question":
                    f"Describe a real project where you used {skill}. What challenges did you face and how did you solve them?",
                    "topic": skill,
                    "difficulty":
                    difficulty,
                    "suggested_answer":
                    f"Candidate should explain practical experience with {skill}.",
                }
            )

        # --------------------------------------------------
        # 3. Experience-based questions
        # --------------------------------------------------

        if experience_years < 2:

            questions.append(
                {
                    "question":
                    "Describe a technical concept you learned recently and how you applied it.",
                    "topic":
                    "Learning Ability",
                    "difficulty":
                    difficulty,
                    "suggested_answer":
                    "Candidate should demonstrate growth mindset.",
                }
            )

        elif experience_years < 5:

            questions.append(
                {
                    "question":
                    "Describe a production issue you solved and the steps you followed.",
                    "topic":
                    "Problem Solving",
                    "difficulty":
                    difficulty,
                    "suggested_answer":
                    "Candidate should demonstrate debugging skills.",
                }
            )

        else:

            questions.append(
                {
                    "question":
                    "How would you mentor junior developers while maintaining delivery timelines?",
                    "topic":
                    "Leadership",
                    "difficulty":
                    difficulty,
                    "suggested_answer":
                    "Candidate should demonstrate technical leadership.",
                }
            )

        # --------------------------------------------------
        # 4. System Design
        # --------------------------------------------------

        if difficulty in [
            "medium",
            "hard",
        ]:

            questions.append(
                {
                    "question":
                    "Design a scalable REST API for a recruitment platform handling thousands of candidates.",
                    "topic":
                    "System Design",
                    "difficulty":
                    difficulty,
                    "suggested_answer":
                    "Candidate should discuss scalability, databases, caching and APIs.",
                }
            )

        # --------------------------------------------------
        # 5. Hard Questions
        # --------------------------------------------------

        if difficulty == "hard":

            questions.append(
                {
                    "question":
                    "How would you design a distributed system capable of processing millions of job applications?",
                    "topic":
                    "Distributed Systems",
                    "difficulty":
                    "hard",
                    "suggested_answer":
                    "Candidate should discuss queues, scalability and fault tolerance.",
                }
            )

        # --------------------------------------------------
        # 6. Behavioral
        # --------------------------------------------------

        questions.append(
            {
                "question":
                "Tell me about a time when you had to learn a completely new technology under a tight deadline.",
                "topic":
                "Behavioral",
                "difficulty":
                "medium",
                "suggested_answer":
                "Candidate should provide a STAR-based example.",
            }
        )

        return questions[
            :num_questions
        ]