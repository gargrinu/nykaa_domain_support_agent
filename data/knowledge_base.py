import os

# Knowledge Base Content:
KNOWLEDGE_BASE = {
    "01_return_window.txt": """
Return windows vary by product category. Beauty products can generally be returned within 7 days of delivery if unused and in their original packaging. Apparel and Footwear items may be returned within 15 days of delivery. Electronics and Home products may be returned within 10 days unless otherwise specified on the product page.
""",

    "02_cod_refund_timelines.txt": """
For Cash on Delivery orders, approved refunds are processed directly to the customer's bank account. Customers are required to provide accurate bank details before refund processing begins. Refunds are typically completed within 5 to 7 business days after the return is approved.
""",

    "03_delivery_slas.txt": """
Standard deliveries are completed within 3 to 7 business days for most serviceable locations. Remote locations may require additional delivery time. During festive seasons or severe weather conditions, delivery timelines may be extended beyond the standard service level agreement.
""",

    "04_reverse_pickup_eligibility.txt": """
Reverse pickup services are available only in selected serviceable pin codes. Products requested for return must be securely packed and ready for collection. If reverse pickup is unavailable in a location, customers may be asked to self-ship the item and provide shipment proof.
""",

    "05_warranty_terms.txt": """
Warranty coverage depends on the product category. Electronics may carry manufacturer warranties ranging from 6 months to 2 years depending on the product. Beauty consumables are generally not covered under warranty, while select beauty devices may include limited warranty protection.
""",

    "06_order_cancellation_policy.txt": """
Orders can be cancelled before they are shipped from the fulfillment center. Once an order has entered the shipping process, cancellation requests may no longer be accepted. Customers may instead initiate a return after delivery if the item is eligible under the return policy.
""",

    "07_loyalty_points_redemption.txt": """
Loyalty points can be redeemed during checkout on eligible purchases. Points cannot typically be exchanged for cash or transferred between customer accounts. If an order is refunded, redeemed loyalty points may be credited back according to the applicable reward program rules.
""",

    "08_payment_failure_retry.txt": """
If a payment attempt fails, customers may retry the payment using the same or a different payment method. Failed transactions are not considered confirmed orders unless payment is successfully completed. Any temporary payment authorization holds are released according to banking timelines.
""",

    "09_size_exchange_policy.txt": """
Size exchanges are available for eligible Apparel and Footwear products. Exchange requests must be initiated within the category-specific return window. The requested replacement size is subject to stock availability at the time the exchange is processed.
""",

    "10_damaged_item_claims.txt": """
Customers receiving damaged items should report the issue within 48 hours of delivery. Supporting photographs of the product and packaging may be required for verification. Once validated, the customer may receive a replacement, refund, or another appropriate resolution.
""",

    "11_international_shipping.txt": """
International shipping is available only in selected countries and regions. Certain product categories may be restricted because of local regulations, customs requirements, or transportation limitations. Customers are responsible for any applicable import duties or taxes unless stated otherwise.
""",

    "12_escalation_matrix.txt": """
Customer support requests are escalated based on issue severity and resolution status. Tier 1 handles routine order and policy inquiries, while Tier 2 reviews returns, refunds, and delivery disputes. Tier 3 manages exceptional cases, regulatory concerns, and unresolved escalations requiring managerial review.
"""
}

# Knowledge Base Creation:
def create_knowledge_base(output_dir="knowledge_base"):
    """
    Create all required knowledge-base documents.
    """

    os.makedirs(output_dir, exist_ok=True)

    for filename, content in KNOWLEDGE_BASE.items():

        file_path = os.path.join(
            output_dir,
            filename
        )

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:
            file.write(content.strip())

    print(
        f"Created {len(KNOWLEDGE_BASE)} knowledge-base documents in '{output_dir}'"
    )

# Main Execution:
if __name__ == "__main__":
    create_knowledge_base()