from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class VolumePriceTierOut(BaseModel):
    min_qty: int
    max_qty: Optional[int] = None
    unit_price: float

    model_config = ConfigDict(from_attributes=True)


class VariantOut(BaseModel):
    id: int
    sku: str
    name: str
    price_base: float
    stock_available: int
    volume_prices: List[VolumePriceTierOut] = []

    model_config = ConfigDict(from_attributes=True)


class ProductListItemOut(BaseModel):
    id: int
    omie_product_code: str
    name: str
    slug: str
    brand: Optional[str] = None
    active: bool

    model_config = ConfigDict(from_attributes=True)


class ProductDetailOut(BaseModel):
    id: int
    omie_product_code: str
    name: str
    slug: str
    brand: Optional[str] = None
    description_marketing: Optional[str] = None
    variants: List[VariantOut]

    model_config = ConfigDict(from_attributes=True)