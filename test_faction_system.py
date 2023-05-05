
# Faction data
faction_data = {
    "faction1": {
        "name": "Faction One",
        "backstory": "Backstory of Faction One",
        "goals": ["Goal 1", "Goal 2"],
        "resources": ["Resource A", "Resource B"],
        "relationships": {
            "faction2": -0.5
        }
    },
    "faction2": {
        "name": "Faction Two",
        "backstory": "Backstory of Faction Two",
        "goals": ["Goal 3", "Goal 4"],
        "resources": ["Resource C", "Resource D"],
        "relationships": {
            "faction1": -0.5
        }
    }
}



# Create a FactionSystem instance
faction_system = FactionSystem(faction_data)

# Add players
faction_system.add_player("Player One")
faction_system.add_player("Player Two")

# Align players with factions
faction_system.align_with_faction("Player One", "faction1")

# Change alignment with a faction
faction_system.change_alignment("Player One", "faction1", 0.2)

# Display player's alignment
faction_system.display_alignment("Player One")