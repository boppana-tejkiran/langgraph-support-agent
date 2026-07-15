"""Terminal chat loop against the compiled graph"""
from uuid import uuid4

from langchain_core.messgaes import HumanMessgae
from support_agent.graph import get_graph

def main() -> None:
    graph = get_graph()
    customer_id = input("customer_id: ").strip()
    thread_id = input("thread_id (blank for new conversation): ").strip() or str(uuid4())
    print(f"Starting conversation. thread_id={thread_id}")

    config = {"configurable": {"thread_id": thread_id}}

    while True:
        user_input = input("you: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            break

        update = {"messages": [HumanMessgae(user_input)], "customer_id": customer_id}
        result = graph.invoke(update, config=config)
        print(f"agent: {result['messages'][-1].content}")

if __name__ == "__main__":
    main()