import yaml
from math import exp

class PriceCalculator():
    
    def __init__(self,  product):
        self.product = product
        self.read_data()

    def read_data(self):
        with open("data.yaml", 'r') as stream:
            self.data = yaml.load(stream)[self.product]

    def calculate_discount(self):
        # check discount calculations, they don't make sense like that.
        stock_discount = min(0.2,  (self.data['stock'] - self.data['desired_stock']) / self.data['desired_stock'] * 0.1)
        expiration_discount = 1 - exp(min(0, self.data['remaining_days'] - self.data['critical_days']) / self.data['critical_days'])
        demand_discount = 1 - self.data['demand']
        self.discount = stock_discount + expiration_discount + demand_discount
        print('stock_discount is %f' %(stock_discount))
        print('expiration discount is %f' %(expiration_discount))
        print('demand discount is %f' %(demand_discount))
        print('total discount is %f' %(self.discount))

    def calculate_price(self):
        self.price = self.data['nominal_price'] * (1 - self.discount)
        print('Nominal price is %f but our dynamic price is %f' %(self.data['nominal_price'],  self.price))

    def update_input(self, stock, remaining_days, demand):
        print('stock %s remaining days %s demand %s' %(stock,  remaining_days,  demand))
        self.data['stock'] = stock
        self.data['remaining_days'] = remaining_days
        self.data['demand'] = demand



if __name__ == "__main__":
    priceCalculator = PriceCalculator('apple')
    priceCalculator.calculate_discount()
    priceCalculator.calculate_price()
    

    
