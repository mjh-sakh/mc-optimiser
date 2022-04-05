import random

import pytest

from mc_optimiser.models.simple_store import SimpleShopModel


@pytest.fixture
def shop():
    return SimpleShopModel(6, days_to_run=10)


@pytest.fixture
def random_state():
    random.seed(10)
    return random.getstate()


def reset_and_run(shop, random_state):
    shop.reset()
    random.setstate(random_state)
    shop.run()


def test_model_runs_and_resets(shop, random_state):
    shop.run()
    res1 = shop.revenue
    assert all([shop.expenses > 0, shop.profit > 0])

    reset_and_run(shop, random_state)
    res2 = shop.revenue
    assert res1 == res2


def test_can_be_changed(shop, random_state):
    changeable_params = {
        'refill_factor',
        'days_to_run',
        'rating',
        'boxes_count',
        'box_capacity',
        'shelf_life',
        'item_cost',
        'item_price',
    }

    shop.run()
    base = (shop.profit, shop.revenue)
    for param in changeable_params:
        shift_size = min(1, int(shop.__dict__[param] * 0.2))
        shop.__dict__[param] -= shift_size
        reset_and_run(shop, random_state)

        assert shop.profit, shop.revenue != base


def test_has_optimum(shop, random_state):
    results = []
    for factor in range(1, 10):
        shop.refill_factor = factor
        reset_and_run(shop, random_state)
        results.append(shop.revenue)

    assert max(results) != min(results)
