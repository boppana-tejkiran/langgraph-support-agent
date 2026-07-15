"""Session registry: let us answer "which thread_ids belong to this customer_id?"

The checkpointer only supports loading history for a single known
thread_id; it ccan't enumerate threads for a customer. Long-term store
namespace (customer_id, "sessions") fills that gap. 
"""