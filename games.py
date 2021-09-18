from aesthetics import *


def rock_paper_scissors() -> (bool, int):
    """Rock paper scissors mini game"""
    clear()
    text = """
RANDOM GENERATOR OVERLOADING PROCEDURE:

LOADING EXTREMELY COMPLEX RANDOM GENERATOR SELECTION ALGORITHM..."""
    slowPrint(text, 0.5)
    loadingBar(20, 0.1)
    loadingBar(20, 0.2)
    loadingBar(20, 0.05)
    # For some reason only the Linux terminal seems to have fast enough
    # default settings for this not to be unbearably slow
    if sysName == "Linux":
        loadingBar(1000, 0.001)
    print()

    ls = ['rock', 'paper', 'scissors']
    gesture = ls[random.randint(0, 2)]
    guess = input('Key in your action, rock, paper, or scissors: ')
    guess = guess.lower()
    print("The enemy showed: " + gesture)
    if guess == 'rock' or guess == 'paper' or guess == 'scissors':
        if guess == 'rock':
            if gesture == 'paper':
                print('You Lose!')
                return False, -20
            elif gesture == 'rock':
                print('You tied.')
                return False, 0
            else:
                print('You Win!')
                return False, 20
        elif guess == 'paper':
            if gesture == 'paper':
                print('You tied.')
                return False, 0
            elif gesture == 'rock':
                print('You Win!')
                return False, 20
            else:
                print('You Lose!')
                return False, -20
        else:
            if gesture == 'paper':
                print('You Win!')
                return False, 20
            elif gesture == 'rock':
                print('You Lose!')
                return False, -20
            else:
                print('You Tied.')
                return False, 0
    else:
        print("Please key in rock, paper or scissors.")
        return rock_paper_scissors()


def hangman() -> (bool, int):
    """Hangman mini game"""
    clear()
    ls = ['space', 'asteroid', 'oxygen', 'rocket', 'elon musk', 'nasa', 'spacesuit', 'alien', 'shuttle', 'reentry',
          'comet', 'meteoroid', 'gravity', 'galaxy', 'milky way', 'blackhole', 'astronaut', 'neil armstrong',
          'constellation',
          'solar system', 'moon', 'dwarf planet', 'pluto', 'mars', 'cosmic', 'space satellite', 'interstellar',
          'wormhole']
    password = ls[random.randint(0, len(ls) - 1)]
    slowPrint("""ATTEMPTING TO OVERCLOCK CORE PROCESSING FEATURES...
""", 0.5)
    loadingBar(20, 0.1)
    slowPrint("""
WARNING: MALICIOUS USER ACTIVITY DETECTED

-------- SECURITY LOCKDOWN -------

YOU HAVE BEEN LOCKED OUT

ENTER YOUR PASSWORD TO REGAIN CONTROL

SECURITY HINT: SPACE-RELATED WORDS""", 0.5)
    # print("Your spacecraft is being hacked, guess the password in a game of hangman to protect your ship! HINT: Space-related words")
    guesses = ''

    turns = 10
    ls = []
    while turns > 0:
        failed = 0
        for letter in password:
            if letter in guesses:
                print(letter)
            else:
                print("_")
                failed += 1
        if failed == 0:
            print("You Win")
            print("The password is: ", password)
            return True, 10
        guess = input("guess a character:")
        while guess in ls:
            print("You already guessed that letter.")
            guess = input("guess a character:")
        ls += [guess]
        print("characters guessed = ", ls)
        guesses += guess
        if guess not in password:
            turns -= 1
            print("Wrong")
            print("You have", + turns, 'more guesses')
            if turns == 0:
                print("You Lose")
                return True, -10


def math_mini_games() -> (bool, int):
    """Math mini game"""
    clear()
    slowPrint("""ATTEMPTING TO ACCESS ACTIVE HULL RECONSTITUTION CAPABILITIES...

""", 0.5)
    loadingBar(20, 0.05)
    slowPrint("""
YOU HAVE EXHIBITED SUSPICIOUS BEHAVIOUR

PROVE THAT YOU ARE HUMAN IN ORDER TO PROCEED

LOADING COMPLICATED MATHEMATICAL QUESTIONS...""", 0.5)

    loadingBar(20, 0.1)

    def askQuestion(level: int, question: str, ans: int, pts: int = 0) -> (bool, int):
        """Function to ask question from questionList below"""
        player_ans = numberMenu("""
LEVEL: {level}
______________________
{question}

Your answer: """.format(level=level, question=question), range(10000000), 0.1)

        if player_ans != ans:
            slowPrint("""
Your answer is wrong. Spaceship has been heavily damaged. Try again!
Press ENTER to continue. """, 0.1)
            input()
            pts -= 50
            return askQuestion(level, question, ans, pts)
        else:
            pts += 50
            return pts

    questionList = {
        1: [1, """
The distance between Planet Sram and Earth is 6km while the distance between Earth and Planet Jupyter is 10km.
If it takes 3 years to reach Planet Sram from Earth, how long does it take to go from Earth to Planet Jupyter?
""",
            5],
        2: [2, """
What is 1207+657 ?
""",
            1864],
        3: [3, """
The total number of passengers ferried by a taxi driver from Monday to Friday was 35. 
The number of passengers ferried on Saturday was 9, while the number of passengers ferried on Sunday was 12.
Find the average number of passengers ferried per day for the entire week.
""",
            8],
        4: [4, """
What is 90 multiplied by 55 ?
""",
            4950],
        5: [5, """
Pikotaro had some black pens and 30 blue pens. 
After he gave away 13 black pens for apples and 8 blue pens for pineapples, he had 80 pens left.
How many black pens did Pikotaro have at first?
""",
            71],
        6: [6, """
Cookie Monster had 48 cookies in a jar. 
For breakfast, he ate 1/4 of the cookies. 
For lunch, he ate 2/3 of the remaining cookies.
How many cookies were left in the jar?
""",
            12],
        7: [7, """
The price of a computer is $1100. Bill buys it at a discount of 25%. 
However, he also uses a $200 gift voucher
How much does Bill still have to pay?
""",
            625],
        8: [8, """
A Gong Cha bubble tea outlet sold twice the number of cups on Saturday than Friday. 
It sold 23 cups fewer on Sunday than Saturday.
If the number of cups sold on Sunday was 97, find the number of cups sold on Friday.
""",
            60],
        9: [9, """
What is 1+2+3+...+100 ?
""",
            5050],
        10: [10, """
At first, John had some $10 notes and $2 notes in the ratio of 3 : 8. 
After exchanging two $10 notes for $2 notes, the ratio of $10 notes to $2 notes became 1 : 3.
Find the amount of money John had.
""",
             736]
    }

    params = questionList.get(random.randint(1, 10))
    finalPts = askQuestion(params[0], params[1], params[2])
    return False, finalPts


def enemyFight() -> (bool, int):
    """Spaceship combat mini game"""

    def receivingEnemyFire() -> None:
        slowPrint("WARNING: RECEIVING FIRE, SYSTEMS DAMAGED", 0.01)
        slowPrint(displayText, 0.1)

    clear()
    maxVal = 20
    minVal = 1
    x = random.randint(minVal, maxVal)
    y = random.randint(minVal, maxVal)
    pts = 0
    slowPrint("""
OPTIMIZING RADAR FOR MICRODEBRIS AVOIDANCE

WARNING: RADAR STEALTH WILL NOT WORK""", 0.5)
    loadingBar(20, 0.05)
    slowPrint("""OPTIMIZATION SUCCESSFUL""", 1)
    time.sleep(2)
    slowPrint("""
WARNING: RECEIVING FIRE FROM ENEMY SPACECRAFT

AUTOMATIC TARGETING SYSTEM DAMAGED

MANUAL TARGETING ENABLED""", 0.5)
    loadingBar(20, 0.05)
    displayText = """
     N
     |
W----+----E
     |
     S
                  + Y coord.
                  ^
                  |
                  |
   TARGETING SYS: +------> + X coord."""
    slowPrint(displayText, 0.1)

    """
    print(
        "Do you have what it takes to get the right co-ordinates? Let's find out!:D \n~~KEY:~~ \nIf you have to move North-East increment your x co-ordinate and y co-ordinate")
    print(
        "If you have to move North-West, increment the value of your y co-ordinate and decrement the value of your x co-ordinate")
    print("If you have to move South-West, decrement both your x and y co-ordinates")
    print("If you have to move South-East, decrement your y co-ordinate and increment your x co-ordinate")
    """
    a = numberMenu("Select an X coordinate:", range(minVal, maxVal + 1))
    b = numberMenu("Select a Y coordinate:", range(minVal, maxVal + 1))

    while True:
        if x != a and y != b:
            receivingEnemyFire()
            pts -= 10
            print("both coordinates are wrong, guess again")

            if (a < x) and (b < y):
                print("you need to move to the North-East")
            elif (a > x) and (b < y):
                print("you need to move to the North-West")
            elif (a < x) and (b > y):
                print("you need to move to the South-East")
            else:
                print("you need to move to the South-West")
            a = numberMenu("enter x:", range(minVal, maxVal + 1))
            b = numberMenu("enter y:", range(minVal, maxVal + 1))

        elif x == a and y != b:
            receivingEnemyFire()
            pts -= 5
            print("the x-coordinate is correct but not the y-coordinate")
            if y < b:
                print("you need to move to the South")
            else:
                print("you need to move to the North")
            b = numberMenu("enter y:", range(minVal, maxVal + 1))


        elif x != a and y == b:
            receivingEnemyFire()
            pts -= 5
            print("the x-coordinate is wrong but the y-coordinate is correct")
            if x < a:
                print("you need to move to the West")
            else:
                print("you need to move to the East")
            a = numberMenu("enter x:", range(minVal, maxVal + 1))


        else:
            print("congrats! you have got both the coordinates! you can move on:)")
            return False, pts


globalGameDict = {
    1: "math_mini_games",
    2: "enemyFight",
    3: "hangman",
    4: "rock_paper_scissors"
}
