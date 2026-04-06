from __future__ import annotations
from typing import List

from sqlalchemy import String, Integer, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Variant(Base):
    __tablename__ = "variants"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    sku: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    omie_sku_code: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    name: Mapped[str] = mapped_column(String(255))

    price_base: Mapped[float] = mapped_column(Numeric(10, 2))
    stock_available: Mapped[int] = mapped_column(Integer)

    active: Mapped[bool] = mapped_column(Boolean, default=True)

    product: Mapped["Product"] = relationship(back_populates="variants")

    volume_price_tiers: Mapped[list["VolumePriceTier"]] = relationship(
        back_populates="variant",
        cascade="all, delete-orphan",
    )

@property
def volume_prices(self) -> List["VolumePriceTier"]:
    tiers = [t for t in (self.volume_price_tiers or []) if getattr(t, "active", True)]
    tiers.sort(key=lambda t: t.min_qty)
    return tiers