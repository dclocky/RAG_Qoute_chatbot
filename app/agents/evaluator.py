from typing import List, Dict, Any


class EvaluatorAgent:

    def __init__(self):
        pass

    def evaluate(self, query: str, offers: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not offers:
            return {"recommendation": None, "offers_evaluated": [], "reasoning": "No offers found"}

        def score(o):
            risk_penalty = 5 if "risk" in o["risk_notes"].lower() else 0
            return -(o["unit_price"] + 0.1 * o["delivery_days"] + risk_penalty)

        for o in offers:
            o["score"] = score(o)

        best = max(offers, key=lambda x: x["score"])
        return {"recommendation": best, "offers_evaluated": offers, "reasoning": ""}

    def reasoning(self, query, offers, best_offer):
        parts = [
            f"{o['supplier']} (${o['unit_price']} / unit, {o['delivery_days']} days, risk: {o['risk_notes']})"
            for o in offers
        ]
        return f"Compared offers: {', '.join(parts)}. Best supplier: {best_offer['supplier']}."
