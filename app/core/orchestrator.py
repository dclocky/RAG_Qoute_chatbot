import uuid
from dataclasses import asdict

from app.agents.extractor import ExtractorAgent
from app.agents.evaluator import EvaluatorAgent
from app.db.vector_db import VectorDatabase


class Orchestrator:

    def __init__(self):
        self.db = VectorDatabase()
        self.extractor = ExtractorAgent()
        self.evaluator = EvaluatorAgent()

    def ingest_quote(self, text: str):
        extracted = self.extractor.extract(text)
        doc_id = str(uuid.uuid4())

        self.db.add(doc_id, text)

        result = asdict(extracted)
        result["id"] = doc_id
        return {"status": "stored", **result}

    def process_query(self, query: str):

        documents = self.db.search(query)
        offers = []

        for d in documents:
            extracted = self.extractor.extract(d["text"])
            entry = asdict(extracted)
            entry["id"] = d["id"]
            offers.append(entry)

        evaluation = self.evaluator.evaluate(query, offers)

        evaluation["reasoning"] = self.evaluator.reasoning(
            query,
            evaluation["offers_evaluated"],
            evaluation["recommendation"]
        )

        return evaluation


orchestrator = Orchestrator()
