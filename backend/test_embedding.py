from app.services.embedding_service import generate_embedding

embedding = generate_embedding(
    "Python FastAPI PostgreSQL Developer"
)

print(len(embedding))