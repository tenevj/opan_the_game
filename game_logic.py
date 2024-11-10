import random
from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class Hex:
    q: int
    r: int

    def neighbors(self) -> List['Hex']:
        directions = [
            (1, 0), (1, -1), (0, -1),
            (-1, 0), (-1, 1), (0, 1)
        ]
        return [Hex(self.q + dq, self.r + dr) for dq, dr in directions]

    def distance(self, other: 'Hex') -> int:
        return (abs(self.q - other.q) + 
                abs(self.q + self.r - other.q - other.r) + 
                abs(self.r - other.r)) // 2

class GameState:
    def __init__(self):
        self.players: Dict[str, Dict] = {}
        self.npcs: Dict[str, Dict] = {}
        self.combat_state = None

    def add_player(self, player_id: str, position: Hex):
        self.players[player_id] = {
            "position": position,
            "stats": {
                "health": 20,
                "attack": 8,
                "defense": 10,
                "armor_class": 5
            }
        }

    def move_entity(self, entity_id: str, new_pos: Hex, is_npc: bool = False):
        entities = self.npcs if is_npc else self.players
        if entity_id in entities:
            current_pos = entities[entity_id]["position"]
            if new_pos in current_pos.neighbors():
                entities[entity_id]["position"] = new_pos
                return True
        return False

    def resolve_combat(self, attacker_id: str, defender_id: str) -> Dict:
        attack_roll = random.randint(1, 20)
        attacker = self.players.get(attacker_id) or self.npcs.get(attacker_id)
        defender = self.players.get(defender_id) or self.npcs.get(defender_id)
        
        if attack_roll >= defender["stats"]["armor_class"]:
            damage = random.randint(1, 8) + 3  # d8+3
            defender["stats"]["health"] -= damage
            return {
                "hit": True,
                "damage": damage,
                "attack_roll": attack_roll
            }
        return {
            "hit": False,
            "damage": 0,
            "attack_roll": attack_roll
        }