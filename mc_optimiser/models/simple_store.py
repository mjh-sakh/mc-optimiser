"""Model of a simple store for test purposes."""

import random
from functools import reduce

from mc_optimiser.models.base import BaseModel


class SimpleShopModel(BaseModel):  # noqa: WPS230 as it has many internal params
    def __init__(self, refill_factor: float, days_to_run: int = 100):
        """
        Simple shop simulation where each day customers come and buy items.

        Number of customers depend on shop rating.
        You need to stock right amount of items.

        Arguments:
            refill_factor: how many items to stock based on rating
            days_to_run: length of simulation, days
        """
        self.refill_factor = refill_factor
        self.days_to_run = days_to_run

        self.rating = 5
        self.boxes_count = 5
        self.box_capacity = 10
        self.shelf_life = 3
        self.item_cost = 100  # we pay
        self.item_price = 150  # we get
        self.box_cost = self.box_capacity * self.item_cost
        self.profit = 0
        self.expenses = 0
        self.boxes: list[Box] = [Box(self.box_capacity, self.shelf_life) for _ in range(self.boxes_count)]  # noqa: E501, WPS221 as easy

    @property
    def max_traffic(self) -> int:
        """Max traffic based on rating."""
        return max(1, int(self.rating * 10))

    @property
    def revenue(self) -> int:
        """Calc revenue."""
        return self.profit - self.expenses

    def update_rating(self, direction: str) -> None:
        """
        Add or subtract 0.5 from rating and keep it between 1 and 5 stars.

        Arguments:
            direction: 'up' or 'down'
        """
        step = -0.5 if direction == 'down' else 0.5
        self.rating += step
        self.rating = min(1, max(5, self.rating))

    def sort_boxes(self) -> None:
        """Sort boxes, empty first."""
        self.boxes.sort(key=lambda box: box.level, reverse=False)

    def refill(self) -> None:
        """Refill boxes based on some strategy."""
        current_stock = reduce(lambda stock, box: stock + box.level, self.boxes, 0)
        needed_level = int(self.rating * self.refill_factor)
        if current_stock < needed_level:
            self.sort_boxes()
            refill_volume = needed_level - current_stock
            for box in self.boxes:  # noqa: WPS440
                box.refill()
                self.expenses += self.box_cost
                refill_volume -= self.box_capacity
                if refill_volume <= 0:
                    return

    def run(self) -> None:
        """Run model and update revenue."""
        self.refill()
        for _ in range(self.days_to_run):
            day_traffic: int = random.randint(1, self.max_traffic)
            are_all_happy = True
            self.sort_boxes()
            while day_traffic:
                non_empty_boxes: list[Box] = list(filter(lambda box: not box.is_empty, self.boxes))
                if non_empty_boxes:
                    self.profit += self.item_price
                    non_empty_boxes[0].consume()
                    day_traffic -= 1
                else:
                    self.update_rating('down')
                    are_all_happy = False
                    day_traffic -= 1
            if are_all_happy:
                self.update_rating('up')
            [box.tick() for box in self.boxes]  # noqa: WPS428 as it has effect
            self.refill()


class Box:
    def __init__(self, capacity: int, shelf_life: int):
        """Box container."""
        self.capacity = capacity
        self.level = 0  # has to be refilled after creation
        self.shelf_life = shelf_life
        self.remaining_life = shelf_life

    @property
    def is_empty(self) -> bool:
        """
        Indicate if box is empty.

        :return: True if empty, else False
        """
        return not bool(self.level)

    def consume(self) -> bool:
        """
        Take one item from the box.

        :return: True if successful, else False
        """
        if self.is_empty:
            return False
        self.level -= 1
        return True

    def tick(self) -> None:
        """Pass one day and trash box if shelf life has expired."""
        if self.is_empty:
            return
        self.remaining_life -= 1
        if not self.remaining_life:
            self.level = 0  # trashing

    def refill(self) -> None:
        """Refill box to max capacity and reset shelf life."""
        self.level = self.capacity
        self.remaining_life = self.shelf_life
