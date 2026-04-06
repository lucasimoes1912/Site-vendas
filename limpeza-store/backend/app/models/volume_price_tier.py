from sqlalchemy import Integer, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

class VolumePriceTier(Base):
    __tablename__= "volume_price_tiers"

    id: Mapped[int] = mapped_column(primary_key=True)
    variant_id: Mapped[int] = mapped_column(ForeignKey("variants.id"))

    min_qty: Mapped[int] = mapped_column(Integer)
    max_qty: Mapped[int | None] = mapped_column (Integer, nullable=True)

    unit_price: Mapped[float] = mapped_column(Numeric(10, 2))

    active: Mapped [bool] = mapped_column(Boolean, default=True)

    variant: Mapped ["Variant"] = relationship(back_populates="volume_price_tiers")