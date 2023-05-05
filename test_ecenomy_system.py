import random
import matplotlib.pyplot as plt
from game.economy_system import EconomySystem


# Example usage
materials = ["A", "B", "C"]
cities = ["City1", "City2", "City3"]
factions = {
    "City1": {"name": "Faction1", "price_modifier": 1.1},
    "City2": {"name": "Faction2", "price_modifier": 0.9},
    "City3": {"name": "Faction3", "price_modifier": 1.0}
}
material_density = {
    "City1": {"A": 20, "B": 40, "C": 60},
    "City2": {"A": 60, "B": 20, "C": 40},
    "City3": {"A": 40, "B": 60, "C": 20}
}

economy = EconomySystem(materials, cities, factions, material_density)
economy._adjust_prices_for_faction_influence()
economy.simulate_trading()
economy.random_event()
print(economy.get_prices("City1"))
print(economy.get_density("City1", "A"))

# Assuming the EconomySystem class and example data are defined as shown above

economy = EconomySystem(materials, cities, factions, material_density)
economy._adjust_prices_for_faction_influence()

# Store the price data for each generation
price_history = {city: {material: [] for material in materials} for city in cities}

# Simulate trading over 100 generations
generations = 200
for generation in range(generations):
    economy.simulate_trading()

    # Trigger a random event every 5 generations
    if generation % 15 == 0:
        economy.random_event()

    # Record the price data
    for city in cities:
        for material in materials:
            price_history[city][material].append(economy.get_prices(city)[material])

# Plot the price data using matplotlib
fig, axs = plt.subplots(len(cities), figsize=(10, 6 * len(cities)))
for i, city in enumerate(cities):
    for material in materials:
        axs[i].plot(price_history[city][material], label=f"Material {material}")
    axs[i].set_title(f"{city} Prices")
    axs[i].set_xlabel("Generation")
    axs[i].set_ylabel("Price")
    axs[i].legend()

plt.tight_layout(h_pad=6.0)
plt.show()
