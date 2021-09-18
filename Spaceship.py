from aesthetics import *


class Spaceship:
    """Singleton: represents the spaceship's health and energy, and its getter/setter methods."""

    def __init__(self, health: int, energy: int) -> None:
        self.health = health
        self.energy = energy

    def getHealth(self) -> int:
        return self.health

    # Simultaneously change health and alert the player
    def changeHealth(self, amount: int, msg: str = "ALERT") -> None:
        self.health += amount
        incOrDec = "increased" if amount > 0 else "decreased" if amount < 0 else "not changed"
        slowPrint(
            msg + ": Spaceship hull integrity has " + incOrDec + " by " + str(amount) + " to: " + str(
                self.getHealth())
        )

    def getEnergy(self) -> int:
        return self.energy

    # Simultaneously change energy and alert the player
    def changeEnergy(self, amount: int, msg: str = "ALERT") -> None:
        # Actually change the energy value
        self.energy += amount
        incOrDec = "increased" if amount > 0 else "decreased" if amount < 0 else "not changed"
        slowPrint(
            msg + ": Power supply has " + incOrDec + " by " + str(amount) + " to: " + str(self.getEnergy())
        )
