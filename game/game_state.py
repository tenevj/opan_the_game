from models import Character

class GameState:
    def __init__(self):
        self.players = {}
        self.npcs = {}
        self.combat_state = None
        self.turn_based_combat = False

    def add_player(self, player_id, name="Player"):
        self.players[player_id] = Character(name)
        return self.players[player_id]

    def add_npc(self, npc_id, name="Enemy"):
        self.npcs[npc_id] = Character(name)
        return self.npcs[npc_id]

    def get_entity(self, entity_id):
        return self.players.get(entity_id) or self.npcs.get(entity_id)

    def start_combat(self, player_id, npc_id):
        self.turn_based_combat = True
        self.combat_state = {
            "player_id": player_id,
            "npc_id": npc_id,
            "current_turn": player_id
        }

    def end_combat(self):
        self.turn_based_combat = False
        self.combat_state = None