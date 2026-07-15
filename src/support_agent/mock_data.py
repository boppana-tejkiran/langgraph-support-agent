"""In-memory mock data standing in for real backend systems (accounts, orders, tickets)."""

ACCOUNTS: dict[str, dict] = {
    "cust_1": {"name": "Priya Shah", "email": "priya@example.com", "subscription": "Pro"},
    "cust_2": {"name": "Alex Kim", "email": "alex@example.com", "subscription": "Free"},
}

ORDERS: dict[str, dict] = {
    "order_100": {"customer_id": "cust_1", "status": "shipped", "total": 49.99, "refused": False},
    "order_101": {"customer_id": "cust_2", "status": "delivered", "total": 19.99, "refunded": False},
}

TICKETS: list[dict] = []