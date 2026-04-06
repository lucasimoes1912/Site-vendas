from app.core.database import SessionLocal
from app.models.product import Product
from app.models.variant import Variant
from app.models.volume_price_tier import VolumePriceTier


def run():
    db = SessionLocal()

    # Limpa dados (somente para dev)
    db.query(VolumePriceTier).delete()
    db.query(Variant).delete()
    db.query(Product).delete()
    db.commit()

    # Produto 1
    produto1 = Product(
        omie_product_code="OMIE-P001",
        name="Detergente Neutro 5L",
        slug="detergente-neutro-5l",
        brand="LimpaMais",
        description_marketing="Detergente neutro concentrado para uso profissional.",
    )

    variante1 = Variant(
        sku="DET-NEU-5L",
        omie_sku_code="OMIE-SKU-001",
        name="Galão 5 Litros",
        price_base=25.90,
        stock_available=120,
    )

    variante1.volume_price_tiers = [
        VolumePriceTier(min_qty=1, max_qty=9, unit_price=25.90),
        VolumePriceTier(min_qty=10, max_qty=49, unit_price=23.90),
        VolumePriceTier(min_qty=50, max_qty=None, unit_price=21.90),
    ]

    produto1.variants.append(variante1)

    # Produto 2
    produto2 = Product(
        omie_product_code="OMIE-P002",
        name="Desinfetante Floral 2L",
        slug="desinfetante-floral-2l",
        brand="Higienix",
        description_marketing="Desinfetante floral para limpeza geral.",
    )

    variante2 = Variant(
        sku="DES-FLO-2L",
        omie_sku_code="OMIE-SKU-002",
        name="Frasco 2 Litros",
        price_base=12.50,
        stock_available=200,
    )

    variante2.volume_price_tiers = [
        VolumePriceTier(min_qty=1, max_qty=19, unit_price=12.50),
        VolumePriceTier(min_qty=20, max_qty=None, unit_price=10.90),
    ]

    produto2.variants.append(variante2)

    db.add_all([produto1, produto2])
    db.commit()
    db.close()

    print("Seed executado com sucesso.")


if __name__ == "__main__":
    run()