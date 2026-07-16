from langchain_core.tools import tool
from support_agent import mock_data

@tool
def create_ticket(customer_id: str, subject: str, description: str) -> str:
    """File a support ticket for a customer."""
    ticket_id = f"ticket_{len(mock_data.TICKETS)+1}"
    mock_data.TICKETS.append(
        {
            "id": ticket_id,
            "customer_id": customer_id,
            "subject": subject,
            "description": description,
            "status": "open",
        }
    )
    return f"Created {ticket_id} (status: open)."

@tool
def process_refund(order_id: str, reason: str) -> str:
    """Process a refund for an order."""
    order = mock_data.ORDERS.get(order_id)
    if not order:
        return f"No order found for order_id={order_id}"
    if order["refunded"]:
        return f"Order {order_id} was already refunded."
    order["refunded"] = True
    return f"Refunded ${order['total']} for order {order_id}. Reason: {reason}"