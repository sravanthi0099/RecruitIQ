"""
Embedding service.
Temporary version to avoid
sentence-transformers dependency issues.
"""

from typing import List


def generate_embedding(text: str) -> List[float]:
    """
    Generate a temporary embedding vector.

    This is a placeholder implementation.
    Replace later with SentenceTransformer.
    """

    return [0.0] * 384