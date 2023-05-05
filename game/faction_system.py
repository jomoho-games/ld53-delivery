class FactionSystem:
    def __init__(self, faction_data):
        self.faction_data = faction_data
        self.base_alignments = {}

    def add_player(self, player_name):
        self.base_alignments[player_name] = {}

    def align_with_faction(self, player_name, faction_key):
        if player_name in self.base_alignments and faction_key in self.faction_data:
            self.base_alignments[player_name][faction_key] = 0

    def change_alignment(self, player_name, faction_key, points):
        if player_name in self.base_alignments and faction_key in self.base_alignments[player_name]:
            self.base_alignments[player_name][faction_key] += points

    def get_alignment(self, player_name):
        total_alignment = {}

        for faction_key in self.faction_data:
            total_alignment[faction_key] = self.base_alignments[player_name].get(faction_key, 0)
            for related_faction, relationship in self.faction_data[faction_key]['relationships'].items():
                total_alignment[faction_key] += self.base_alignments[player_name].get(related_faction, 0) * relationship

        return total_alignment

    def display_alignment(self, player_name):
        if player_name in self.base_alignments:
            print(f"{player_name}'s Alignment:")
            total_alignment = self.get_alignment(player_name)
            for faction_key, points in total_alignment.items():
                print(f"{faction_key}: {points}")

