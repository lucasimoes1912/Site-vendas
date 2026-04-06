from typing import Dict, Set, Literal, get_args

OrderStatus = Literal["created", "confirmed", "cancelled", "invoiced", "shipped", "delivered",]

ORDER_STATUSES = set(get_args(OrderStatus))

ALLOWED_TRANSITIONS: Dict[OrderStatus, Set[OrderStatus]] = {
    "created": {"confirmed", "cancelled"},
    "confirmed": {"invoiced", "cancelled"},
    "invoiced": {"shipped"},
    "shipped": {"delivered"},
    "delivered": set(),
    "cancelled": set(),
}

def can_transition(current: OrderStatus, new: OrderStatus) -> bool:
    return new in ALLOWED_TRANSITIONS.get(current, set())

