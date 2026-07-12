"""Text processing utilities."""

import re
from typing import List, Dict
from loguru import logger


class TextProcessor:
    """Service for text processing and normalization."""

    @staticmethod
    def normalize_text(text: str) -> str:
        """
        Normalize text for processing.
        
        Args:
            text: Input text
            
        Returns:
            Normalized text
        """
        if not text:
            return ""

        # Convert to lowercase
        text = text.lower()

        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        # Remove special characters but keep alphanumeric and spaces
        text = re.sub(r'[^a-z0-9\s\-]', '', text)

        return text

    @staticmethod
    def extract_sentences(text: str) -> List[str]:
        """
        Extract sentences from text.
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        if not text:
            return []

        # Split by common sentence endings
        sentences = re.split(r'[.!?]+', text)

        # Clean and filter
        sentences = [s.strip() for s in sentences if s.strip()]

        return sentences

    @staticmethod
    def extract_email_addresses(text: str) -> List[str]:
        """
        Extract email addresses from text.
        
        Args:
            text: Input text
            
        Returns:
            List of email addresses
        """
        if not text:
            return []

        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(pattern, text)

        return list(set(emails))  # Remove duplicates

    @staticmethod
    def extract_phone_numbers(text: str) -> List[str]:
        """
        Extract phone numbers from text.
        
        Args:
            text: Input text
            
        Returns:
            List of phone numbers
        """
        if not text:
            return []

        pattern = r'\b[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}\b'
        phones = re.findall(pattern, text)

        return list(set(phones))  # Remove duplicates

    @staticmethod
    def extract_urls(text: str) -> List[str]:
        """
        Extract URLs from text.
        
        Args:
            text: Input text
            
        Returns:
            List of URLs
        """
        if not text:
            return []

        pattern = r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)'
        urls = re.findall(pattern, text)

        return list(set(urls))  # Remove duplicates

    @staticmethod
    def calculate_text_similarity(text1: str, text2: str) -> float:
        """
        Calculate similarity between two texts using word overlap.
        
        Args:
            text1: First text
            text2: Second text
            
        Returns:
            Similarity score (0-1)
        """
        if not text1 or not text2:
            return 0.0

        words1 = set(TextProcessor.normalize_text(text1).split())
        words2 = set(TextProcessor.normalize_text(text2).split())

        if not words1 or not words2:
            return 0.0

        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))

        return intersection / union if union > 0 else 0.0

    @staticmethod
    def get_word_frequency(text: str, top_n: int = 10) -> Dict[str, int]:
        """
        Get word frequency distribution.
        
        Args:
            text: Input text
            top_n: Number of top words to return
            
        Returns:
            Dictionary of word frequencies
        """
        if not text:
            return {}

        words = TextProcessor.normalize_text(text).split()
        
        # Filter out common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during'
        }

        filtered_words = [w for w in words if w not in stop_words and len(w) > 2]

        # Count frequencies
        frequency = {}
        for word in filtered_words:
            frequency[word] = frequency.get(word, 0) + 1

        # Sort and get top N
        sorted_freq = sorted(frequency.items(), key=lambda x: x[1], reverse=True)
        
        return dict(sorted_freq[:top_n])


text_processor = TextProcessor()
