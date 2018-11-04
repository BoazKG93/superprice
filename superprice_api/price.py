import yaml
from math import exp


class PriceCalculator():

    def __init__(self, product):
        self.product = product


    def calculate_discount(self):
        # check discount calculations, they don't make sense like that.
        stock_discount = min(0.2, (self.product.stock - self.product.desired_stock) / self.product.desired_stock * 0.1)
        expiration_discount = 1 - exp(
            min(0, self.product.remaining_days - self.product.critical_days) / self.product.critical_days)
        demand_discount = 1 - self.product.demand
        self.discount = stock_discount + expiration_discount + demand_discount

    def calculate_price(self):
        self.price = self.product.price * (1 - self.discount)

    def update_input(self, stock, remaining_days, demand):
        self.product.stock = stock
        self.product.remaining_days = remaining_days
        self.product.demand = demand


if __name__ == "__main__":
    priceCalculator = PriceCalculator('apple')
    priceCalculator.calculate_discount()
    priceCalculator.calculate_price()


