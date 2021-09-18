from aesthetics import *


class PowerSource:
    """Each instance represents a powersource that the player has found"""

    def __init__(self, timeToReach: int, powerChance: int, currDangerLevel: int) -> None:
        time.sleep(0.1)
        slowPrint("POWER SOURCE DETECTED")  # Print message when powersource is "found" (is actually just generated)
        self.timeToReach = timeToReach
        self.powerChance = powerChance
        self.currDangerLevel = currDangerLevel

    def getTimeToReach(self) -> int:
        return self.timeToReach

    def getPowerChance(self) -> int:
        return self.powerChance

    def harvestPower(self) -> (int, int):
        """Called when player decides to harvest this powersource"""
        slowPrint("TRAVELLING TO SELECTED POWER SOURCE")
        loadingBar(40, self.getTimeToReach()/50)  # Loading bar duration scales with distance to powersource
        slowPrint("WARNING: {timeToReach} DAYS HAVE BEEN ADDED TO THE TIME REMAINING".format(
            timeToReach=str(self.getTimeToReach())))

        chanceToDud = random.randint(0, 100) < self.currDangerLevel * 10  # Chance to dud scales with difficulty level
        if chanceToDud:
            slowPrint("ALERT: POWER SOURCE HAS BEEN DISCOVERED TO BE A DUD")
            return self.getTimeToReach(), 0
        else:
            amt = random.randint(0, self.getPowerChance())
            slowPrint("POWER HARVESTED SUCCESSFULLY FROM OBJECT: {amt}".format(amt=str(amt)))
            return self.getTimeToReach(), amt
