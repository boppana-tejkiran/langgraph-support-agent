from langchain_core.messages import HumanMessage
from tests.conftest import requires_real_openai_key

@requires_real_openai_key
def test_routes_faq_question(test_graph):
    result = test_graph.invoke(
        {"messages": [HumanMessage("What's your return window?")], "customer_id": "cust_1", "escalated": False},
        config={"configurable": {"thread_id": "t1"}},
    )
    assert result["next"] == "faq"

@requires_real_openai_key
def test_routes_order_status(test_graph):
    result = test_graph.invoke(
        {"messages": [HumanMessage("What is the status of order_100")], "customer_id": "cust_1", "escalated": False},
        config={"configurable":{"thread_id": "t2"}},
    )
    assert result["next"] == "account"

@requires_real_openai_key
def test_routes_refund_request(test_graph):
    result = test_graph.invoke(
        {
            "messages": [HumanMessage("I want a refund for order_101, it arrived damaged")],
            "customer_id": "cust_2",
            "escalated": False,
        },
        config={"configurable": {"thead_id": "t3"}},
    )
    assert result["next"] == "ticketing"

@requires_real_openai_key
def test_routes_explicit_escaltion(test_graph):
    result = test_graph.invoke(
        {
            "messages": [HumanMessage("This is ridiculous, let me talk to a real person")],
            "customer_id": "cust_1",
            "escalated": False,
        },
        config={"configurable": {"thread_id": "t4"}},
    )
    assert result["next"] == "escalation"
    assert result["escalated"] is True