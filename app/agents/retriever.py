from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer


class RetrieverAgent:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        if not query.strip():
            return []
        return []
