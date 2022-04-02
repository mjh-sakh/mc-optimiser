import pytest
from mc_optimiser.models.simple_store import SimpleShopModel

def test_model_runs():
    shop = SimpleShopModel(6, days_to_run=100)
    shop.run()
    print(shop.revenue)
    assert shop.revenue != 0


def test_has_optimum():
    results = []
    for factor in range(1, 10):
        shop = SimpleShopModel(factor)
        shop.run()
        results.append(shop.revenue)

    print(results)
    assert max(results) != min(results)

