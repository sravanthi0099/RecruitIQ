"""Embedding utilities for semantic search."""

from typing import List
import numpy as np
from loguru import logger


class EmbeddingService:
    """Service for generating and managing embeddings."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Initialize embedding service.
        
        Args:
            model_name: HuggingFace model name
        """
        self.model_name = model_name
        self.model = None
        self._initialize_model()

    def _initialize_model(self):
        """Initialize embedding model."""
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Embedding model loaded: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            self.model = None

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for text.
        
        Args:
            text: Input text
            
        Returns:
            Embedding vector
        """
        if not self.model:
            logger.warning("Embedding model not initialized")
            return []

        try:
            embedding = self.model.encode(text, convert_to_numpy=False)
            return embedding.tolist() if hasattr(embedding, 'tolist') else embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return []

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of input texts
            
        Returns:
            List of embedding vectors
        """
        if not self.model:
            logger.warning("Embedding model not initialized")
            return []

        try:
            embeddings = self.model.encode(texts, convert_to_numpy=False)
            return [e.tolist() if hasattr(e, 'tolist') else e for e in embeddings]
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return []

    @staticmethod
    def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Similarity score (0-1)
        """
        if not vec1 or not vec2:
            return 0.0

        arr1 = np.array(vec1)
        arr2 = np.array(vec2)

        dot_product = np.dot(arr1, arr2)
        norm1 = np.linalg.norm(arr1)
        norm2 = np.linalg.norm(arr2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(dot_product / (norm1 * norm2))

    @staticmethod
    def euclidean_distance(vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate euclidean distance between two vectors.
        
        Args:
            vec1: First vector
            vec2: Second vector
            
        Returns:
            Distance
        """
        if not vec1 or not vec2:
            return float('inf')

        arr1 = np.array(vec1)
        arr2 = np.array(vec2)

        return float(np.linalg.norm(arr1 - arr2))


embedding_service = EmbeddingService()
