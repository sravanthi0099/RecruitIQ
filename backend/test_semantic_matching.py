from app.services.semantic_matching_service import (
    semantic_matching_service
)

resume = """
Python Developer
FastAPI
PostgreSQL
Docker
"""

job = """
Looking for backend engineer
with API development and database experience
"""

score = semantic_matching_service.calculate_semantic_match(
    resume,
    job
)

print(score)