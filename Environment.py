import os
from typing import List

from PowerSource import PowerSource
import games
from aesthetics import *
import Spaceship


class Environment:
    """Singleton: Manager class that represents most background variables and processes that govern gameplay"""

    def __init__(self, dangerLevel: int, daysLeft: int, dayCount: int, spaceShip: Spaceship) -> None:
        self.dangerLevel = dangerLevel
        self.daysLeft = daysLeft
        self.dayCount = dayCount
        self.spaceShip = spaceShip

    saveFileBeginning = "MERIDIANSTATE_"
    saveFileExtension = ".qsr"
    gameDict = games.globalGameDict

    def getDangerLevel(self) -> int:
        return self.dangerLevel

    def modulateDangerLevel(self) -> None:
        """Called every day to update the difficulty level according to the number of days left"""

        # Subfunction to update dangerLevel
        def changeDangerLevel(newLevel: int, msg: str) -> None:
            # Only do anything if new dangerLevel is different from the current one
            if newLevel != self.dangerLevel:
                incOrDec = "EASIER" if newLevel < self.dangerLevel else "HARDER"
                self.dangerLevel = newLevel
                slowPrint("""
{msg}

DANGER LEVEL: {dangerLevel}. FATE WILL GO {incOrDec} ON YOU IN MYSTERIOUS WAYS.

PRESS ENTER TO ACKNOWLEDGE

""".format(msg=msg, dangerLevel=newLevel, incOrDec=incOrDec))
                input()

        # Control flow for when to change dangerLevel depends on number of daysLeft
        if self.getDaysLeft() > 15:
            changeDangerLevel(1, "NO MYSTERIOUS PARTICLE FIELD DETECTED, SYSTEMS AT MAX")
        elif self.getDaysLeft() > 10 and self.getDaysLeft() <= 15:
            changeDangerLevel(2, "MYSTERIOUS PARTICLE FIELD WITHIN SCANNER RANGE, BRACE SYSTEMS")
        elif self.getDaysLeft() > 5 and self.getDaysLeft() <= 10:
            changeDangerLevel(3, "ALERT: WITHIN OUTER REGION OF MYSTERIOUS PARTICLE FIELD")
        elif self.getDaysLeft() > 0 and self.getDaysLeft() <= 5:
            changeDangerLevel(4, "WARNING: SPACECRAFT DEEP INSIDE MYSTERIOUS PARTICLE FIELD")

    def getDaysLeft(self) -> int:
        return self.daysLeft

    # Simultaneously change daysLeft and alert the player
    def changeDaysLeft(self, amount: int) -> None:
        self.daysLeft += amount
        incOrDec = "increased" if amount > 0 else "decreased"
        slowPrint(
            "Days left to reach has " + incOrDec + " by " + str(amount) + " to: " + str(self.getDaysLeft())
        )

    def getDayCount(self) -> int:
        return self.dayCount

    # Simultaneously change dayCount and alert the player
    def changeDayCount(self, amount: int) -> None:
        self.dayCount += amount
        incOrDec = "increased" if amount > 0 else "decreased"
        slowPrint(
            "DAY: " + str(self.getDayCount())
        )

    def sitRep(self) -> None:
        """Main menu and entry point for player interaction"""
        screenStatic()
        statusReport = """
SITUATION REPORT
DAY {dayCount}
DAYS OF TRAVEL LEFT: {daysLeft}
____________________________________

HULL INTEGRITY: {health}
ENERGY: {energy}
____________________________________""".format(
            dayCount=str(self.getDayCount()),
            daysLeft=str(self.getDaysLeft()),
            health=str(self.spaceShip.getHealth()),
            energy=str(self.spaceShip.getEnergy())
        )
        slowPrint(statusReport, 0.1)  # Print status report

        # Warn player if health or energy are critical
        if self.spaceShip.getHealth() < 20: slowPrint("WARNING: HULL INTEGRITY CRITICAL")
        if self.spaceShip.getEnergy() < 20: slowPrint("WARNING: POWER FAILURE IMMINENT")

        mainMenu = """
PLEASE SELECT AN ACTION:
1) Scan for power sources
2) Perform task
3) Skip day
4) DO NOT PRESS
5) Save Game
6) Load Game
ENTER CHOICE: """
        choice = numberMenu(mainMenu, range(7), 0.1)

        # Control flow depends on player input
        if choice == 1:
            self.scanForPowerSources()
        elif choice == 2:
            self.playGameByKey()
        elif choice == 3:
            slowPrint("CRUISE MODE ENGAGED")
            self.skipDays()
            slowPrint("DAY SKIPPED")
            slowPrint("CRUISE MODE DISENGAGED")
            return
        elif choice == 4:  # Self-destruct and quit game
            text = """
SELF DESTRUCT SEQUENCE INITIATED

I HOPE YOU'RE HAPPY WITH YOURSELF

ENJOY BEING STRANDED


"""
            slowPrint(text, 0.5)
            for i in range(100):
                print("KABOOM")

            quit(0)
        elif choice == 5:
            self.saveGame()
            self.sitRep()  # Run sitRep again since saving game should not take up a day
        elif choice == 6:
            self.runSavedGame()
            self.sitRep()  # Run sitRep again since loading game should not take up a day

    def scanForPowerSources(self) -> None:
        """Player-interactive function to scan for power sources"""

        def rollChance(numberOfRolls: int) -> int:
            """Calculate how many powersources are generated. numberOfRolls is the maximum number
            of possible powersources that the player can roll for. For each successful roll, that
             powersource is "found"."""
            successCount = 0
            for i in range(numberOfRolls):
                # For each possible powersource, roll chance to see if it is successfully found
                rngNum = random.randint(0, 100)
                scaledChance = 10 * self.getDangerLevel()
                if scaledChance < rngNum:
                    successCount += 1  # Add 1 to the number of successful finds
            return successCount

        def checkForPowerSources() -> List[PowerSource]:
            """Generate power sources"""
            powerSourceList = []
            for i in range(rollChance(10 - self.getDangerLevel())):  # Maximum number of powersources scales with difficulty level

                # In general, time to reach increases with difficulty level
                timeToReach = random.randint(0, 20 * self.getDangerLevel())

                # In general, max power per powersource decreases with difficulty level
                powerChance = random.randint(0, 50 - (5 * self.getDangerLevel()))

                # Instantiate new powersource with corresponding attributes
                newPowerSource = PowerSource(timeToReach, powerChance, self.getDangerLevel())
                powerSourceList.append(newPowerSource)

            return powerSourceList

        def minusEnergy() -> List[PowerSource]:
            """Deduct energy for scanning"""
            self.spaceShip.changeEnergy(- 5 * self.getDangerLevel(), "POWER DRAINED FOR SCANNER")
            newList = checkForPowerSources()
            return newList

        def displayLoop(powerSourceList: List[PowerSource]) -> (int, int):
            """Player-interactive menu to select powersource to harvest, or to decline action"""
            index = 1
            slowPrint("-------- PROCESSING SENSOR INFO --------")
            time.sleep(2)
            for powerSource in powerSourceList:
                time.sleep(0.05)
                slowPrint("""
TIME TO REACH POTENTIAL POWER SOURCE {index} : {timeToReach}
MAXIMUM POWER FROM SOURCE {index}: {powerChance}""".format(
                    index=str(index),
                    timeToReach=str(powerSource.getTimeToReach()),
                    powerChance=str(powerSource.getPowerChance())))
                index += 1
            time.sleep(1)
            print()
            text = "ENTER YOUR CHOICE, OR " + str(index) + " TO DECLINE: "
            choice = numberMenu(text, range(index + 1))

            if choice == index:
                return 0, 0
            elif 0 < choice < index:
                return powerSourceList[choice - 1].harvestPower()
            else:
                displayLoop(powerSourceList)

        slowPrint("SCANNING FOR POWER SOURCES")
        loadingBar(20, 0.1)
        print()
        result = displayLoop(minusEnergy())  # result is a tuple of (bool, int)
        powerAmt = result[1]  # int component
        self.spaceShip.changeEnergy(powerAmt, "POWER HARVEST OUTCOME")

        dayAmt = result[0]
        self.changeDaysLeft(dayAmt)
        slowPrint("PRESS ENTER TO CONTINUE")
        input()

    def playGameByKey(self, isAutomated: bool = False, autoChoice: int = "ERROR") -> None:
        """Plays a mini game. Player-interactive by default, but can be automated with isAutomated and autoChoice
        in order to force the player into a mini game for random events."""

        text = """
SELECT A TASK:
1) Active Hull Reconstitution (Math Problem Game)\t\t<HULL INTEGRITY>
2) Microdebris Avoidance Radar (Spaceship Combat)\t\t<HULL INTEGRITY>
3) Core Processor Overclocking (Space Hangman)\t\t\t<POWER>
4) Randomized Generator Overclocking (Rock Paper Scissors)\t<POWER>
ENTER CHOICE: """
        choice = autoChoice
        if not isAutomated:
            choice = numberMenu(text, range(5), 0.25)

        game = getattr(games, self.gameDict[choice])
        result = game()

        amt = result[1]
        if result[0]:
            self.spaceShip.changeEnergy(amt, "TASK OUTCOME")
        else:
            self.spaceShip.changeHealth(amt, "TASK OUTCOME")

        input("PRESS ENTER KEY TO CONTINUE")

    def skipDays(self) -> None:
        """Allows the player to select a number of days to skip"""

        text = """
ENTER NUMBER OF DAYS TO SKIP: """
        choice = numberMenu(text, range(100))
        for i in range(choice - 1):
            if not self.checkForEndGame():
                slowPrint("DAY SKIPPED")
                self.wearAndTear()
        time.sleep(0.5)

    def checkForEndGame(self) -> bool:
        """Checks if the game should end and exits if so"""

        endGame = False
        if self.spaceShip.getHealth() <= 0:
            endGame = True
            slowPrint("CATASTROPHIC HULL BREACH: CRAFT DESTROYED" + scatterPrint("DESTROYED"))
            slowPrint("------- YOU LOSE -------")

        if self.spaceShip.getEnergy() <= 0:
            endGame = True
            slowPrint("CATASTROPHIC POWER FAILURE: SYSTEM FAILURE" + scatterPrint("FAILURE"))
            slowPrint("------- YOU LOSE -------")

        if self.getDaysLeft() <= 0:
            endGame = True
            slowPrint("DESTINATION REACHED")
            slowPrint("------- YOU WIN -------")

        if endGame:
            quit(0)
        else:
            return endGame

    def wearAndTear(self) -> None:
        """Takes care of day-to-day background processes"""

        baseEnergyDrain = -5
        scaledEnergyDrain = baseEnergyDrain * self.getDangerLevel()  # Scale daily energy drain with difficulty level
        self.spaceShip.changeEnergy(scaledEnergyDrain, "END-OF-DAY POWER DRAIN")

        self.dayCount += 1
        self.daysLeft -= 1
        self.modulateDangerLevel()
        randomEventRoll = 20 > random.randint(0, 100 - (self.getDangerLevel() * 20))
        if randomEventRoll:
            slowPrint("""
WARNING: RANDOM EVENT OCCURRING

BRACE YOURSELF

PRESS ENTER TO CONTINUE""", 0.1)
            input()
            gameChoice = random.randint(1, len(self.gameDict))
            self.playGameByKey(True, gameChoice)

    def normalDayEnd(self) -> None:
        """Main game loop"""
        while not self.checkForEndGame():
            self.sitRep()
            self.wearAndTear()
            slowPrint("PRESS ENTER TO CONTINUE TO THE NEXT DAY")
            input()

    def saveGame(self) -> None:
        """Player-interactive function to save game with custom filename"""
        clear()
        slowPrint("""
QUANTUM STATE PRESERVATION IS BEING ATTEMPTED

ENTER NAME OF QUANTUM STATE REPOSITORY: """, 0.5)
        name = input()
        if not os.path.exists("{saveFileBeginning}{name}{saveFileExtension}".format(
                saveFileBeginning=self.saveFileBeginning,
                name=name,
                saveFileExtension=self.saveFileExtension)):
            newFile = open("{saveFileBeginning}{name}{saveFileExtension}".format(
                saveFileBeginning=self.saveFileBeginning,
                name=name,
                saveFileExtension=self.saveFileExtension
            ),
                "w")
            newDict = {
                "health": self.spaceShip.getHealth(),
                "energy": self.spaceShip.getEnergy(),
                "dangerLevel": self.getDangerLevel(),
                "daysLeft": self.getDaysLeft(),
                "dayCount": self.getDayCount()
            }

            content = ""
            for key in newDict:
                content += """{key} {val}
""".format(key=key, val=newDict[key])

            newFile.write(content)
        else:
            slowPrint("File already exists")

        slowPrint("""
RUNNING QUANTUM STATE PRESERVATION ENGINE

ATTEMPTING TO TAKE QUANTUM STATE SNAPSHOT

WARNING: BRACE FOR IMPACT...
""", 0.5)
        loadingBar(20, 0.1)
        slowPrint("PRESS ENTER TO CONTINUE")
        input()  # Pause and wait for player to press enter

    def runSavedGame(self) -> None:
        """Player-interactive function to run a saved game"""

        def getDict(targetFile: str) -> dict:
            """Extract save data from file into dictionary"""
            newDict = {}
            with open(targetFile) as f:
                for lineNumber, line in enumerate(f):
                    key = line.split()[0]
                    val = line.split()[1]
                    newDict[key] = int(val)
            return newDict

        def unsafeReplaceAllValues(someDict: dict) -> None:
            """Replace all environment values with the extracted save file data"""
            self.spaceShip.health = someDict["health"]
            self.spaceShip.energy = someDict["energy"]
            self.dangerLevel = someDict["dangerLevel"]
            self.daysLeft = someDict["daysLeft"]
            self.dayCount = someDict["dayCount"]

        clear()
        slowPrint("""
WARNING: QUANTUM STATE RECOVERY IS BEING ATTEMPTED

SEARCHING FOR AVAILABLE .QSR FILES""", 0.5)

        fileCount = 0
        fileDict = {}
        currDir = os.getcwd()
        for file in os.listdir(currDir):
            if file.endswith(self.saveFileExtension):
                fileCount += 1
                d = getDict(file)
                fileDict[fileCount] = d
                dString = ""
                for key in d:
                    dString += "\t{key}: {val}\n".format(key=key, val=str(d[key]))
                slowPrint("""
{fileCount}: {file}
{dString}""".format(fileCount=fileCount, file=file, dString=dString), 0.1)

        choice = numberMenu("SELECT FILE: ", range(1, fileCount + 1))
        unsafeReplaceAllValues(fileDict[choice])
