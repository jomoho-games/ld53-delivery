import random

class EconomySystem:
    def __init__(self, materials, cities, factions, material_density):
        self.materials = materials
        self.cities = cities
        self.factions = factions
        self.material_density = material_density
        self.prices = self._initialize_prices()
        self.supply = self._initialize_supply()

    def _initialize_prices(self):
        prices = {}
        for city in self.cities:
            city_prices = {}
            for material in self.materials:
                base_price = 100 - self.material_density[city][material]
                city_prices[material] = base_price
            prices[city] = city_prices
        return prices

    def _initialize_supply(self):
        supply = {}
        for city in self.cities:
            city_supply = {}
            for material in self.materials:
                city_supply[material] = 0
            supply[city] = city_supply
        return supply

    def _adjust_prices_for_faction_influence(self):
        for city, faction in self.factions.items():
            for material, base_price in self.prices[city].items():
                self.prices[city][material] = base_price * faction["price_modifier"]

    def trade(self, city, material, amount):
        self.supply[city][material] += amount
        self.prices[city][material] *= (1 - 0.01 * amount)

    def simulate_trading(self):
        for city in self.cities:
            for material in self.materials:
                random_amount = random.randint(-5, 5)
                if self.supply[city][material] + random_amount >= 0:
                    self.trade(city, material, random_amount)

    def random_event(self):
        affected_city = random.choice(self.cities)
        affected_material = random.choice(self.materials)
        price_change = random.uniform(0.5, 1.5)
        self.prices[affected_city][affected_material] *= price_change

    def get_prices(self, city):
        return self.prices[city]

    def get_density(self, city, material):
        return self.material_density[city][material]


def distance(vec1, vec2):
    return (vec2 - vec1).length()

def calculate_material_density(materials, cities):
    material_density = defaultdict(lambda: defaultdict(int))

    # Count the density of each material within the radius for each city
    for city in cities:
        city_pos = city['pos']
        city_radius = city['radius']
        city_area = math.pi * city_radius**2

        material_count = defaultdict(int)

        for material_obj in materials:
            material_type = material_obj.material
            material_amount = material_obj.amount
            material_pos = material_obj.rect.center
            dist = (material_pos - city_pos).length()
            if dist <= city_radius:
                material_count[material_type] += material_amount

        # Calculate the density by dividing the count by the area
        for material_type, count in material_count.items():
            material_density[city['name']][material_type] = count / city_area

    return material_density