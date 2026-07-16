from langchain_core.tools import tool
from support_agent import mock_data

@tool
def lookup_account(customer_id: str) -> str:
    """Look up a customer's account details by customer_id."""
    account = mock_data.ACCOUNTS.get(customer_id)
    return str(account) if account else f"No account found for customer_id={customer_id}"

@tool
def lookup_order(order_id: str) -> str:
    """Look up an order's status and details by order_id."""
    order = mock_data.ORDERS.get(order_id)
    return str(order) if order else f"No order found for order_id={order_id}"

