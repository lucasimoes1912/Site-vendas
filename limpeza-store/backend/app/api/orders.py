from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from typing import Optional

from app.core.database import get_db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate, OrderListResponse
from app.core.orders_workflow import ALLOWED_TRANSITIONS, can_transition, OrderStatus

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("", response_model=OrderListResponse)
def list_orders(
    db:Session = Depends(get_db),
    status: Optional[OrderStatus] =None,
    limit: int = 20,
    offset: int = 0,
):
    limit = max(1, min(limit,100))
    offset = max(0, offset)

    base_stmt = select(Order)

    if status:
        base_stmt = base_stmt.where(Order.status == status)

    total_stmt = select(func.count()).select_from(base_stmt.subquery())
    total = db.execute(total_stmt).scalar_one()

    stmt = base_stmt.order_by(Order.created_at.desc()).limit(limit).offset(offset)
    items = db.execute(stmt).scalars().all()

    return{
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.post("", response_model=OrderResponse, status_code=201)
def create_order(payload: OrderCreate, db: Session = Depends(get_db)):
    if not payload.items:
        raise HTTPException(status_code=400, detail="Order must have at least one item")

    order = Order(
        customer_name=payload.customer_name,
        customer_phone=payload.customer_phone,
        delivery_type=payload.delivery_type,
        delivery_address=payload.delivery_address,
        notes=payload.notes,
        status="created",
    )

    db.add(order)
    db.flush()  # gera order.id

    for item in payload.items:
        order_item = OrderItem(
            order_id=order.id,
            variant_id=item.variant_id,
            sku=item.sku,
            name=item.name,
            qty=item.qty,
            unit_price=item.unit_price,
        )
        db.add(order_item)

    db.commit()
    db.refresh(order)
    return order

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    stmt = (
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.id == order_id)
    )
    order = db.execute(stmt).scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.patch("/{order_id}/status", response_model=OrderResponse)
def updated_order_status(order_id: int, payload: OrderStatusUpdate, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    current = order.status
    new = payload.status

    if current not in ALLOWED_TRANSITIONS:
        raise HTTPException(
            status_code=409,
            detail=f"Order has unknown current status '{current}'. Cannot transition safely.",
        )
    
    if not can_transition(current, new):
        allowed = sorted(list(ALLOWED_TRANSITIONS[current]))
        raise HTTPException(
            status_code=409,
            detail={
                "error": "invalid_status_transition",
                "current": current,
                "requested": new,
                "allowed": allowed,
            },
        )

    order.status = new
    db.add(order)
    db.commit()
    db.refresh(order)
    return order