import json
from pydantic import BaseModel

class OrderStatusResponse(BaseModel):

    record_id: str
    status: str
    order_value_inr: int
    escalation_score: float
    escalation_recommended: bool

# Load Dataset:
def load_orders():
    with open("data/orders.json", "r", encoding="utf-8") as file:
        return json.load(file)

# Dataset Threshold Calculation:
def calculate_dataset_threshold():

    orders = load_orders()

    scores = []

    for order in orders:
        score = calculate_escalation_score(
            order["delayed_shipment"],
            order["days_since_created"]
        )

        scores.append(score)

    scores.sort()

    percentile_80_index = int(
        0.8 * len(scores)
    )

    return scores[
        percentile_80_index
    ]

# Escalation Score Calculation:
def calculate_escalation_score(
    delayed_shipment: bool,
    days_since_created: int
):

    normalized_recency = (days_since_created / 30)
    delay_score = (1.0 if delayed_shipment else 0.0)
    escalation_score = ((0.7 * delay_score) + (0.3 * normalized_recency))

    return round(escalation_score, 2)

# Tool:
def check_order_status(
    record_id: str
):

    orders = load_orders()

    order = next(
        (
            order
            for order in orders
            if order["record_id"]
            == record_id
        ),
        None
    )

    if not order:
        return {
            "success": False,
            "error": "Order not found."
        }

    escalation_score = (
        calculate_escalation_score(
            order["delayed_shipment"],
            order["days_since_created"]
        )
    )

    ESCALATION_THRESHOLD = calculate_dataset_threshold()
    print(f"Escalation Threshold: {ESCALATION_THRESHOLD}")

    response = OrderStatusResponse(
        record_id=order["record_id"],
        status=order["status"],
        order_value_inr=order["order_value_inr"],
        escalation_score=escalation_score,
        escalation_recommended=(escalation_score >= ESCALATION_THRESHOLD)
    )

    return response.model_dump()

# Test:
if __name__ == "__main__":

    result = check_order_status("ORD0019")

    print(result)