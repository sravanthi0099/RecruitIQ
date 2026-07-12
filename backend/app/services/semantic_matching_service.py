from sklearn.metrics.pairwise import cosine_similarity

from app.services.embedding_service import generate_embedding


class SemanticMatchingService:

    @staticmethod
    def calculate_semantic_match(
        resume_text: str,
        job_description: str
    ) -> float:

        resume_embedding = generate_embedding(
            resume_text
        )

        job_embedding = generate_embedding(
            job_description
        )

        score = cosine_similarity(
            [resume_embedding],
            [job_embedding]
        )[0][0]

        return round(score * 100, 2)


semantic_matching_service = SemanticMatchingService()