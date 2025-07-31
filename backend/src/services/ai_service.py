"""AI service for generating summaries using OpenAI."""
import openai
from ..config import settings
from ..exceptions import OpenAIError


class AIService:
    """Service for AI-powered text summarization."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        if not settings.OPENAI_API_KEY:
            raise OpenAIError("OpenAI API key not configured")
        
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    
    def generate_summary(self, text: str) -> str:
        """Generate AI summary of the provided text.
        
        Args:
            text: The text to summarize
            
        Returns:
            Generated summary in Ukrainian
            
        Raises:
            OpenAIError: If API call fails
        """
        if not text.strip():
            return "No text content found in the document."
        
        # Truncate text if too long
        truncated_text = text[:12000] if len(text) > 12000 else text
        
        prompt = (
            "Provide a concise summary of this document in Ukrainian language (max 500 words):\n\n"
            f"{truncated_text}"
        )
        
        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=settings.OPENAI_MAX_TOKENS,
                temperature=settings.OPENAI_TEMPERATURE,
            )
            
            summary = response.choices[0].message.content
            return summary.strip() if summary else "Failed to generate summary."
            
        except Exception as e:
            raise OpenAIError(f"OpenAI API error: {str(e)}")