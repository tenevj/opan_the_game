import random

class Character:
    def __init__(self, name, health=20, attack=8, defense=10, armor_class=5):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.armor_class = armor_class
        self.position = {"q": 0, "r": 0}  # Hex coordinates

    def roll_attack(self):
        return random.randint(1, 20)

    def calculate_damage(self):
        return random.randint(1, 8) + 3  # d8+3 format

    def is_alive(self):
        return self.health > 0

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
        return self.is_alive()