# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys
from typing import List

import aesthetics
from Spaceship import Spaceship
from Environment import Environment

# Testing receiving energy, not used
def bogusGame1():
    print("GAME1 STARTING")
    stuff = input("Hello there type something")
    print(stuff)
    print("GAME1 COMPLETE")
    return True, 10


# Testing receiving health, not used
def bogusGame2():
    print("GAME2 STARTING")
    stuff = input("Hello there type something")
    print(stuff)
    print("GAME2 COMPLETE")
    return False, 20


def argvProcessing(argv: List[str]) -> None:
    """Process command line arguments"""

    def checkKeyAndValInDict(dictionary: dict, key: str, targetList: List[str]):
        """Function to check if either a dictionary key or its corresponding value is in some list"""
        return key in targetList or dictionary[key] in targetList

    # Dictionary of valied command line arguments and their shortforms
    validArgvList = {"--skipIntro": "-s",
                     "--noCrawl": "-n",
                     "--noClear": "-c",
                     "--help": "-h"}

    # Handle --help option
    if checkKeyAndValInDict(validArgvList, "--help", argv):
        print("""
USAGE: python3 main.py <options>
(Use your own installation of python, but must be run with python 3.5 and later)

-s or --skipIntro to skip intro sequence
-n or --noCrawl to stop most text printing character-by-character
-c or --noClear to prevent most attempts to clear the terminal screen (NOTE: it will still attempt to clear once on startup of the game)
-h or --help to display this help

WARNING: this program detects OS through platform.system().
It recognizes "Windows", "Linux", and "Darwin" (MacOS).

It assumes Windows terminals have a "cls" command, and Linux and MacOS have "clear".

It will still run with no OS detected, but aesthetics will be affected.

More information in aesthetics.py""")
        exit(0)  # Exit with error code 0

    # Handle --noCrawl option
    if checkKeyAndValInDict(validArgvList, "--noCrawl", argv):
        aesthetics.NO_CRAWL = True
    else:
        aesthetics.NO_CRAWL = False

    # Handle --noClear option
    if checkKeyAndValInDict(validArgvList, "--noClear", argv):
        aesthetics.NO_CLEAR = True
    else:
        aesthetics.NO_CLEAR = False

    # Handle --skipIntro option
    if checkKeyAndValInDict(validArgvList, "--skipIntro", argv):
        pass
    else:
        # Play intro sequence if it is not skipped.
        # This first call to startUpSeq always attempts to clear the screen
        aesthetics.startUpSeq()


def main(argv: List[str]) -> None:
    """Main function to initialize objects and start game loop"""
    aesthetics.clear()  # Clear screen on game start

    # Process command-line arguments
    argvProcessing(argv)

    # Instantiate Spaceship
    spaceShip = Spaceship(health=100,
                          energy=100,)

    # Instantiate Environment
    environment = Environment(dangerLevel=1,
                              daysLeft=20,
                              dayCount=1,
                              spaceShip=spaceShip)

    # Start main game loop
    environment.normalDayEnd()


# Python-specific way to get command-line arguments
if __name__ == '__main__':
    main(sys.argv[1:])  # Cull useless arguments
