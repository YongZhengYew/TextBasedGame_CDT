import platform
import random
import subprocess
import time
import functools

NO_CRAWL = False
NO_CLEAR = False

# Set default values
sysName = platform.system()
CMD_CLEAR_SCREEN = "ERROR"
SLOWPRINT_DEF_CHARDELAY = 0
SCREENSTATIC_NO_LOOPS = 5
STARTUPSEQ_NO_LOOPS = 5

# Assign OS-specific values if possible
if sysName == "Windows":
    CMD_CLEAR_SCREEN = "cls"
    SLOWPRINT_DEF_CHARDELAY = 0.000001
    SCREENSTATIC_NO_LOOPS = 20
    STARTUPSEQ_NO_LOOPS = 5
elif sysName == "Linux" or sysName == "Darwin":
    CMD_CLEAR_SCREEN = "clear"
    SLOWPRINT_DEF_CHARDELAY = 0.005
    SCREENSTATIC_NO_LOOPS = 500
    STARTUPSEQ_NO_LOOPS = 20


def clear() -> None:
    """Clear the terminal screen"""
    if NO_CLEAR:
        pass
    else:
        try:
            if CMD_CLEAR_SCREEN != "ERROR":
                # Call the OS-specific command to clear the terminal
                subprocess.call(CMD_CLEAR_SCREEN, shell=True)
            else:
                pass
        except FileNotFoundError:
            pass


def slowPrint(longString: str, strDelay: float = 0.0, charDelay: float = SLOWPRINT_DEF_CHARDELAY) -> None:
    """Print text character-by-character, line-by-line"""
    if NO_CRAWL:
        charDelay = 0

    # Split text by newlines
    strArray = longString.split("\n")
    for string in strArray:
        if charDelay:  # If there is a charDelay, loop through each character
            for char in string:
                print(char, end="", flush=True)
                time.sleep(charDelay)
            print()  # newline in between strings
        else:  # Avoid the for-loop to save time if no charDelay is present
            print(string)
        time.sleep(strDelay)


def loadingBar(num: int, delay: float, char: str = "*") -> None:
    """Create a progress bar effect"""
    for i in range(num):
        print(char, end=" ", flush=True)
        time.sleep(delay)


def scatterPrint(text: str = None, minWidth: int = 0, maxWidth: int = 58, repetition: int = 10) -> str:
    """Print specific words in a scattered fashion across the screen"""
    # Concatenate one string with repeated elements of text,
    # and then reduce them into one long string with randomized numbers of spaces in between
    return functools.reduce(lambda acc, x: acc + x + " " * random.randint(minWidth, maxWidth),
                            [text + "\n"] * repetition)


def screenStatic() -> None:
    """Simulate a static effect on the terminal screen by rapidly printing underscores"""
    clear()
    for i in range(SCREENSTATIC_NO_LOOPS):
        # Avoid the static effect if NO_CLEAR is set, but do print newlines to at least somewhat clear the screen
        if not NO_CLEAR:
            # Print strings with random numbers of "_", and insert random numbers of newlines in between
            slowPrint(random.randint(0, 50) * "_", 0.00000000001, 0)
        # Combination of print and slowPrint seem to give a nice effect at high speed
        # as compared to reduction method in scatterPrint
        print(random.randint(0, 2) * "\n")
    clear()


def numberMenu(text: str, span: range, speed: float = 0.5) -> int:
    """Generic function for ensuring valid numerical player input"""
    choice = "ERROR"
    isFirstLoop = True  # Since choice is initialized to "ERROR", avoid printing "INVALID INPUT" if in first loop
    while choice not in span:
        try:
            msg = text if isFirstLoop else "INVALID INPUT!\n" + text
            isFirstLoop = False
            slowPrint(msg, speed)
            choice = int(input())
        except ValueError:
            clear()
            choice = "ERROR IN EXCEPT"  # Debugging purposes
    return choice


def startUpSeq() -> None:
    """Introduce the game to the player"""

    tutorialText = """
You were stranded on the wild planet Cornucopia. after days of searching the skies for possible help,
you finally manage to establish a link to an autonomous spacecraft light years out.

Your only hope is to take remote control of it and help it survive long enough to save you.
20 days is all it should take.

Everyday, power drains from the spaceship. If this runs out, so does your luck.
Obviously, the spaceship must arrive with its hull intact. Scrap metal won't help you off your planet.

Scan for power sources for larger boosts of power, however this comes with a risk. You not only add days to your counter
(by travelling to said source) but you run the risk of finding an empty power source. Do this at your own peril.

Complete tasks to help you regain power and hull integrity. If you fail these tasks, you suffer a penalty.

You may choose to skip days, but remember, this won't save you from random events.

Difficulty level increases as you get closer to your final destination.
"""
    slowPrint(tutorialText, 0.1, 0.01)
    slowPrint("PRESS ENTER TO ATTEMPT TO ESTABLISH RADIO LINK WITH REMOTE SPACECRAFT AND POWER IT ON")
    input()
    clear()

    text1 = """
power on: failed
""" * STARTUPSEQ_NO_LOOPS
    slowPrint(text1, 0.001)
    slowPrint("power on: SUCCESS ----- BACKUP GENERATOR ONLINE")

    text2 = """
ALERT: BOOT SEQUENCE INITIATED
ACCESSING MERIDIAN AUTONOMOUS SPACECRAFT SYSTEM

RECEIVING REMOTE INSTRUCTION...

ALERT: DESTINATION SET FOR <PLANET> ----- X332-0 "CORNUCOPIA"
TIME TAKEN FOR TRAVEL: 20 DAYS

FULL MANUAL CONTROL REQUESTED
Please enter your password: """
    slowPrint(text2, 0.5)
    time.sleep(0.5)

    # Slowly print a random password from the hangman mini game to simulate it being typed in by the player character
    ls = ['space', 'asteroid', 'oxygen', 'rocket', 'elon musk', 'nasa', 'spacesuit', 'alien', 'shuttle', 'reentry',
          'comet', 'meteoroid', 'gravity', 'galaxy', 'milky way', 'blackhole', 'astronaut', 'neil armstrong',
          'constellation',
          'solar system', 'moon', 'dwarf planet', 'pluto', 'mars', 'cosmic', 'space satellite', 'interstellar',
          'wormhole']
    # We are deliberately avoiding using the slowPrint function here so that this "manual typing"
    # effect does not get affected by NO_CRAWL
    for char in ls[random.randint(0, len(ls) - 1)]:
        print(char, end="", flush=True)
        time.sleep(0.25)

    text3 = """
FULL MANUAL CONTROL GRANTED

Linking Backup CLI to POWER SYSTEMS...
Linking Backup CLI to TASK MONITOR...
Linking Backup CLI to CORE SYSTEM CONTROL... """
    slowPrint(text3, 0.1)
    loadingBar(20, 0.2)
    text4 = """Link Success
Restarting Backup CLI to set changes..."""
    slowPrint(text4, 0.5)
    loadingBar(20, 0.1)

    # Clear the screen before starting game proper
    clear()
