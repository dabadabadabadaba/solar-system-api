from time import monotonic_ns
from flask import Blueprint

class Planet:
    def __init__(self, id, name, description, moons):
        self.id = id
        self.name = name
        self.description = description
        self.moons = moons


planets = [
    Planet(1, "Mars", "the Red Planet", ["Deimos", "Phobos"]),
    Planet(2, "Mercury", "the smallest planet", []),
    Planet(3, "Earth", "home", ["Moon"])
    ]

