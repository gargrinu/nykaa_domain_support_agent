import random
from collections import Counter
import json

# Dataset Configuration:
SEED = 42
NUM_ORDERS = 50

CATEGORY = {
    "Beauty": 0.35,
    "Apparel": 0.20,
    "Home": 0.15,
    "Footwear": 0.15,
    "Electronics": 0.15
}

STATUS = {
    "Placed": 0.15,
    "Shipped": 0.25,
    "Delivered": 0.35,
    "Returned": 0.15,
    "Refunded": 0.10
}

MIN_ORDER_VALUE = 199
MAX_ORDER_VALUE = 24999

DELAY_PROBABILITY = 0.20


# Dataset Generation:
def generate_orders(seed=SEED):
    """
    Deterministic order dataset generator.
    Continues generating until all assignment validation criteria are satisfied.
    """

    random.seed(seed)

    while True:

        orders = []

        for i in range(NUM_ORDERS):

            category = random.choices(
                population=list(CATEGORY.keys()),
                weights=list(CATEGORY.values()),
                k=1
            )[0]

            status = random.choices(
                population=list(STATUS.keys()),
                weights=list(STATUS.values()),
                k=1
            )[0]

            order = {
                "record_id": f"ORD{i + 1:04d}",
                "category": category,
                "status": status,
                "order_value_inr": random.randint(
                    MIN_ORDER_VALUE,
                    MAX_ORDER_VALUE
                ),
                "days_since_created": random.randint(
                    0,
                    30
                ),
                "delayed_shipment": (
                    random.random() < DELAY_PROBABILITY
                )
            }

            orders.append(order)

        # Validation Checks
        category_counts = Counter(
            order["category"]
            for order in orders
        )

        status_counts = Counter(
            order["status"]
            for order in orders
        )

        delayed_count = sum(
            order["delayed_shipment"]
            for order in orders
        )

        delayed_percentage = (
            delayed_count / NUM_ORDERS
        ) * 100

        categories_valid = all(
            category_counts[category] >= 3
            for category in CATEGORY
        )

        statuses_valid = all(
            status_counts[status] >= 1
            for status in STATUS
        )

        delay_valid = (
            10 <= delayed_percentage <= 30
        )

        if (
            categories_valid
            and statuses_valid
            and delay_valid
        ):
            return (
                orders,
                category_counts,
                status_counts,
                delayed_percentage
            )

# Save Dataset to JSON:
def save_dataset(orders, filename="orders.json"):
    """
    Save the generated dataset to a JSON file.
    """

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(
            orders,
            file,
            indent=4,
            ensure_ascii=False
        )

    print(f"\nDataset saved to: {filename}")

# Main Execution:
if __name__ == "__main__":

    # Generating Dataset:
    (
        ORDERS,
        category_counts,
        status_counts,
        delayed_percentage
    ) = generate_orders()

    save_dataset(
        ORDERS,
        "data/orders.json"
        )

    # Reporting Dataset Summary:
    print("NYKAA ORDER DATASET SUMMARY:")

    print(f"\nSeed: {SEED}")
    print(f"Total Orders: {len(ORDERS)}")

    print("\nCATEGORY COUNTS:")

    for category in CATEGORY:
        print(
            f"{category}: "
            f"{category_counts[category]}"
        )

    print("\nSTATUS COUNTS:")

    for status in STATUS:
        print(
            f"{status}: "
            f"{status_counts[status]}"
        )

    print("\nDELAYED SHIPMENT STATISTICS:")

    delayed_count = sum(
        order["delayed_shipment"]
        for order in ORDERS
    )

    print(
        f"Delayed Orders: "
        f"{delayed_count}"
    )

    print(
        f"Delayed Percentage: "
        f"{delayed_percentage:.2f}%"
    )

    print("\nVALIDATION RESULTS:")

    print(
        f"All categories >= 3 records: "
        f"{all(category_counts[c] >= 3 for c in CATEGORY)}"
    )

    print(
        f"All statuses >= 1 record: "
        f"{all(status_counts[s] >= 1 for s in STATUS)}"
    )

    print(
        f"Delayed shipment between 10%-30%: "
        f"{10 <= delayed_percentage <= 30}"
    )

# Loading Dataset from JSON:
def load_dataset(filename="orders.json"):
    """
    Load orders from JSON file.
    """

    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)