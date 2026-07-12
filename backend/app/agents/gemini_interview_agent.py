from typing import Dict, Any

from app.agents.base_agent import BaseAgent
from app.services.groq_service import groq_service


class GeminiInterviewAgent(BaseAgent):

    def __init__(self):
        super().__init__(
            name="GroqInterviewAgent",
            version="2.0.0"
        )

    async def execute(
        self,
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:

        candidate_profile = input_data.get(
            "candidate_profile",
            {}
        )

        job_profile = input_data.get(
            "job_profile",
            {}
        )

        skill_gap_profile = input_data.get(
            "skill_gap_profile",
            {}
        )

        difficulty = input_data.get(
            "difficulty",
            "medium"
        )

        num_questions = input_data.get(
            "num_questions",
            10
        )

        prompt = f"""
You are a Senior Technical Interviewer.

Generate interview questions for a candidate.

=========================
JOB ROLE
=========================

{job_profile.get("role", "")}

=========================
REQUIRED SKILLS
=========================

{job_profile.get("required_skills", [])}

=========================
CANDIDATE PROFILE
=========================

{candidate_profile}

=========================
SKILL GAPS
=========================

{skill_gap_profile}

Rules:

1. Questions MUST be based on the JOB ROLE.
2. Prioritize REQUIRED SKILLS.
3. Ask questions about MISSING SKILLS.
4. Include practical real-world scenarios.
5. Include behavioral questions.
6. Include system design questions if applicable.
7. Avoid generic textbook questions.
8. Match difficulty to candidate experience.
9. Generate exactly {num_questions} questions.
10. At least:
   - 4 technical questions
   - 2 practical scenario questions
   - 2 skill-gap questions
   - 2 behavioral questions

Return ONLY valid JSON.

{{
  "questions": [
    {{
      "question": "",
      "topic": "",
      "difficulty": "",
      "reason": ""
    }}
  ]
}}
"""

        result = await groq_service.generate_json(
            prompt
        )

        return result