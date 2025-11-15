import re
from dataclasses import dataclass
from sentence_transformers import SentenceTransformer
from typing import Any


@dataclass
class ExtractedOffer:
    supplier: str
    item: str
    unit_price: float
    delivery_days: int
    risk_notes: str


class ExtractorAgent:

    def __init__(self, llm: Any = None):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def extract(self, text: str) -> ExtractedOffer:
        return ExtractedOffer(
            supplier=self._supplier(text),
            item=self._item(text),
            unit_price=self._unit_price(text),
            delivery_days=self._delivery_days(text),
            risk_notes=self._risk(text)
        )

    def _supplier(self, text):
        match = re.search(r"Supplier\s+([A-Za-z\s&]+)", text)
        return match.group(1).strip() if match else "Unknown Supplier"

    def _item(self, text):
        match = re.search(r"(?:Item|Product)\s*[:\-]?\s*(.+)", text)
        return match.group(1).strip() if match else "Unknown Item"

    def _unit_price(self, text):
        match = re.search(r"\$?(\d+\.?\d*)", text)
        return float(match.group(1)) if match else 0.0

    def _delivery_days(self, text):
        match = re.search(r"(\d+)\s*(?:days|calendar days|business days)", text, re.I)
        return int(match.group(1)) if match else 0

    def _risk(self, text):
        return text.split("Internal Note")[-1].strip() if "Internal Note" in text else "No Internal Note"
