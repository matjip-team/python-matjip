from functools import lru_cache
from app.services.ai_service import generate_rule_based_comment

@lru_cache(maxsize=500)
def cached_ai_comment(question: str, summary: str):
    return generate_rule_based_comment(question, summary)
