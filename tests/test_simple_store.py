import pytest
from mc_optimiser.models.simple_store import SimpleShopModel

@pytest.fixture
def shop():
    return SimpleShopModel(6, days_to_run=10)

def test_model_runs_and_resets(shop):
    shop.run()
    print(shop.revenue)
    assert all([shop.expenses > 0, shop.profit > 0])

    shop.reset()
    assert all([shop.expenses == 0, shop.profit == 0])
    assert sum(box.level for box in shop.boxes) == 0


def test_has_optimum():
    results = []
    for factor in range(1, 10):
        shop = SimpleShopModel(factor)
        shop.run()
        results.append(shop.revenue)

    print(results)
    assert max(results) != min(results)
