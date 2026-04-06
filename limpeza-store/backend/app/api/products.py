from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Query
from sqlalchemy import or_
from sqlalchemy import func
from fastapi import HTTPException
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.product import Product
from app.models.variant import Variant
from app.schemas.product import ProductListItemOut, ProductDetailOut
from app.schemas.pagination import Page

router = APIRouter(prefix="/products", tags=["products"])

@router.get("", response_model=Page[ProductListItemOut])
def list_products(
    db: Session = Depends(get_db),
    q: str | None = Query(default=None, description="Busca por nome/slug"),
    brand: str | None = Query(default=None, description="Filtrar por marca"),
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
):
    base_stmt = select(Product).where(Product.active == True)  # noqa: E712

    if q:
        like = f"%{q}%"
        base_stmt = base_stmt.where(
            or_(
                Product.name.ilike(like),
                Product.slug.ilike(like),
            )
        )

    if brand:
        base_stmt = base_stmt.where(Product.brand == brand)

    # total (sem limit/offset)
    total_stmt = select(func.count()).select_from(base_stmt.subquery())
    total = db.execute(total_stmt).scalar_one()

    # items paginados
    items_stmt = base_stmt.order_by(Product.id).limit(limit).offset(offset)
    items = db.scalars(items_stmt).all()

    return Page[ProductListItemOut](
        items=items,
        total=total,
        limit=limit,
        offset=offset,
    )

@router.get("/{slug}", response_model=ProductDetailOut)
def get_product(slug: str, db: Session = Depends(get_db)):
    stmt = (
        select(Product)
        .where(Product.slug == slug, Product.active == True)  # noqa: E712
        .options(
            selectinload(Product.variants)
            .selectinload(Variant.volume_price_tiers)
        )
    )

    product = db.scalars(stmt).first()

    if not product:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    return product