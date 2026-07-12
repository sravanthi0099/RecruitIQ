"""Input validation utilities."""

from typing import Any, List
from loguru import logger


class ValidationService:
    """Service for input validation."""

    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email address.
        
        Args:
            email: Email address to validate
            
        Returns:
            True if valid, False otherwise
        """
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_phone_number(phone: str) -> bool:
        """
        Validate phone number.
        
        Args:
            phone: Phone number to validate
            
        Returns:
            True if valid, False otherwise
        """
        import re
        # Simple validation for common phone formats
        pattern = r'^[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,9}$'
        return bool(re.match(pattern, phone.replace(' ', '')))

    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Validate URL.
        
        Args:
            url: URL to validate
            
        Returns:
            True if valid, False otherwise
        """
        import re
        pattern = r'^https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)$'
        return bool(re.match(pattern, url))

    @staticmethod
    def validate_string_length(text: str, min_length: int = 1, max_length: int = 255) -> bool:
        """
        Validate string length.
        
        Args:
            text: Text to validate
            min_length: Minimum length
            max_length: Maximum length
            
        Returns:
            True if length is valid, False otherwise
        """
        if not text:
            return min_length == 0
        return min_length <= len(text) <= max_length

    @staticmethod
    def validate_list_length(items: List[Any], min_length: int = 1, max_length: int = 100) -> bool:
        """
        Validate list length.
        
        Args:
            items: List to validate
            min_length: Minimum length
            max_length: Maximum length
            
        Returns:
            True if length is valid, False otherwise
        """
        if not items:
            return min_length == 0
        return min_length <= len(items) <= max_length

    @staticmethod
    def validate_numeric_range(value: float, min_value: float = 0, max_value: float = 100) -> bool:
        """
        Validate numeric range.
        
        Args:
            value: Value to validate
            min_value: Minimum value
            max_value: Maximum value
            
        Returns:
            True if value is in range, False otherwise
        """
        return min_value <= value <= max_value

    @staticmethod
    def sanitize_string(text: str) -> str:
        """
        Sanitize string to remove potentially harmful content.
        
        Args:
            text: Text to sanitize
            
        Returns:
            Sanitized text
        """
        if not text:
            return ""

        # Remove HTML tags
        import re
        text = re.sub(r'<[^>]+>', '', text)

        # Remove SQL keywords
        sql_keywords = ['DROP', 'DELETE', 'INSERT', 'UPDATE', 'SELECT']
        for keyword in sql_keywords:
            if keyword in text.upper():
                logger.warning(f"Potential SQL injection attempt: {keyword}")
                text = text.replace(keyword, '')

        return text.strip()

    @staticmethod
    def validate_skills_list(skills: List[str]) -> List[str]:
        """
        Validate and clean skills list.
        
        Args:
            skills: List of skills
            
        Returns:
            Cleaned skills list
        """
        if not skills:
            return []

        cleaned = []
        for skill in skills:
            # Remove leading/trailing whitespace
            skill = skill.strip()
            
            # Validate length
            if 1 <= len(skill) <= 100:
                cleaned.append(skill)
            else:
                logger.warning(f"Skill '{skill}' is too long or too short")

        return cleaned

    @staticmethod
    def validate_experience_years(years: float) -> bool:
        """
        Validate experience years.
        
        Args:
            years: Years of experience
            
        Returns:
            True if valid, False otherwise
        """
        return 0 <= years <= 100


validation_service = ValidationService()
