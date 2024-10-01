################################################
# Title     : Wheel of Fortune Game
# Author    : balarcode
# Version   : 1.0
# Date      : 1st October 2024
# File Type : Python Script / Program
# File Test : Verified on Python 3.12.6
# Comments  : Game rules are provided below.
#             1) There are 'num_human' human players and 'num_computer' computer players.
#             2) In each round of the game, the players try to guess a phrase.
#                2.1) Players see the category and an obscured version of the phrase containing hidden characters as underscores and correctly guessed characters.
#                     Players also see previously guessed characters which are not in the phrase.
#                2.2) During their turn, a player spins the wheel to determine a prize amount and:
#                     2.2.a) If the wheel lands on a cash square, a player may guess any letter, guess the complete phrase or simply pass their turn. The player may exit from the game as well.
#                     2.2.b) If the wheel lands on "lose a turn", the player loses their turn and the game moves on to the next player.
#                     2.2.c) If the wheel lands on "bankrupt", the player loses their turn and loses their money. However, they keep all of the prizes they have won so far.
#                2.3) The turns or rounds continue until the entire phrase is revealed (or if any player guesses the complete phrase correctly).
#
# All Rights Reserved.
################################################

import json
import random
import time
import os

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
VOWELS = 'AEIOU'
VOWEL_COST = 250

# NOTE: Use the below code snippet to figure out the absolute path to the working directory.
#       Failure to do so will lead to program failure while reading files.
cwd = os.getcwd() # Get the current working directory
files = os.listdir(cwd) # Get all the files and sub-directories in that directory
print("Files in {}: {}".format(cwd, files))
working_directory = cwd + "/Python/wheel_of_fortune/"
print("Working directory is: {}".format(working_directory))

################################################
# Class Definitions
################################################
# Class to represent a Wheel of Fortune player
class WOFPlayer:
    def __init__(self, name):
        self.name = name
        self.prizeMoney = 0
        self.prizes = []
    def addMoney(self, amt):
        self.prizeMoney = self.prizeMoney + amt
    def goBankrupt(self):
        self.prizeMoney = 0
    def addPrize(self, prize):
        self.prizes.append(prize)
    def __str__(self):
        return "{} (${})".format(self.name, self.prizeMoney)

# Derived class to represent a Wheel of Fortune player (human)
class WOFHumanPlayer(WOFPlayer):
    def __init__(self, name):
        super().__init__(name)
    def getMove(self, category, obscuredPhrase, guessed):
        promptString = """
{}

Category: {}
Phrase:   {}
Guessed:  {}

Guess a letter, phrase, or type 'exit' or 'pass': """.format(super().__str__() , category, obscuredPhrase, ', '.join(sorted(guessed)))
        print(promptString)
        userinp = input() # Prompt the user to enter an input
        return userinp

# Derived class to represent a Wheel of Fortune player (computer)
class WOFComputerPlayer(WOFPlayer):
    SORTED_FREQUENCIES = 'ZQXJKVBPYGFWMUCLDRHSNIOATE'
    def __init__(self, name, level):
        super().__init__(name)
        self.level = level
    def smartCoinFlip(self):
        rand_number = random.randint(1, 10)
        if (rand_number > self.level):
            return False
        elif (rand_number <= self.level):
            return True
    def getPossibleLetters(self, guessed):
        possibleLetters = []
        for c in LETTERS:
            if ((c not in guessed) and (c not in VOWELS)):
                possibleLetters.append(c)
            if ((c not in guessed) and (self.prizeMoney >= VOWEL_COST) and (c in VOWELS)):
                possibleLetters.append(c)
        return possibleLetters
    def getMove(self, category, obscuredPhrase, guessed):
        possibleLetters = self.getPossibleLetters(guessed)
        coinFlip = self.smartCoinFlip()
        if (possibleLetters == []):
            print("Returning pass\n")
            return 'pass'
        if (coinFlip == True): # Good move
            possibleLettersL = ''
            for l in possibleLetters:
                possibleLettersL = possibleLettersL+l
            # Do a pick based on the highest frequency character in self.SORTED_FREQUENCIES
            for i in range(len(self.SORTED_FREQUENCIES)-1, 0, -1):
                if (self.SORTED_FREQUENCIES[i] in possibleLettersL):
                    print("Good move: {}\n".format(self.SORTED_FREQUENCIES[i]))
                    return self.SORTED_FREQUENCIES[i]
        elif (coinFlip == False): # Bad move
            possibleLettersL = ''
            for l in possibleLetters:
                possibleLettersL = possibleLettersL+l
            # Do a random pick
            randomLetter = random.choice(possibleLettersL)
            print("Bad move: {}\n".format(randomLetter))
            return randomLetter
        else:
            print("Returning pass\n")
            return 'pass'

################################################
# Function Definitions
################################################
# Repeatedly asks the user for a number between min & max (inclusive) with a user prompt
def getNumberBetween(prompt, min, max):
    """Repeatedly asks the user for a number between min and max (inclusive) with a user prompt."""
    userinp = input(prompt) # Ask for the first time

    while True:
        try:
            n = int(userinp) # Try casting to an integer
            if n < min:
                errmessage = 'Must be at least {}'.format(min)
            elif n > max:
                errmessage = 'Must be at most {}'.format(max)
            else:
                return n
        except ValueError: # The user didn't enter a number
            errmessage = '{} is not a number.'.format(userinp)

        # If we haven't gotten a number yet, add the error message and ask again
        userinp = input('{}\n{}'.format(errmessage, prompt))

# Spins the wheel of fortune wheel to give a random prize
def spinWheel():
    """Simulates spinning the wheel of fortune and returns a dictionary with a random prize"""
    with open(working_directory + "wheel.json", 'r') as f:
        wheel = json.loads(f.read())
        return random.choice(wheel)

# Returns a category & phrase (as a tuple) to guess
def getRandomCategoryAndPhrase():
    """Returns a tuple with a random category and phrase for players to guess"""

    with open(working_directory + "phrases.json", 'r') as f:
        phrases = json.loads(f.read())
        category = random.choice(list(phrases.keys()))
        phrase   = random.choice(phrases[category])
        return (category, phrase.upper())

# Returns an obscure phrase for players to guess
def obscurePhrase(phrase, guessed):
    """
    Given a phrase and a list of guessed letters, returns an obscured version
    Example:
        guessed: ['L', 'B', 'E', 'R', 'N', 'P', 'K', 'X', 'Z']
        phrase:  "GLACIER NATIONAL PARK"
        returns> "_L___ER N____N_L P_RK"
    """
    rv = ''
    for s in phrase:
        if (s in LETTERS) and (s not in guessed):
            rv = rv+'_'
        else:
            rv = rv+s
    return rv

# Returns the current state of the game
def showBoard(category, obscuredPhrase, guessed):
    """Returns a string representing the current state of the game"""
    return """
Category: {}
Phrase:   {}
Guessed:  {}""".format(category, obscuredPhrase, ', '.join(sorted(guessed)))

# Request a player for a move until a valid one is given
def requestPlayerMove(player, category, guessed):
    """Request a player for a move until a valid one is given"""
    while True:
        time.sleep(0.1) # Added so that any feedback is printed out before the next prompt
        move = player.getMove(category, obscurePhrase(phrase, guessed), guessed)
        print("move: {}".format(move))
        move = move.upper()
        if move == 'EXIT' or move == 'PASS':
            return move
        elif len(move) == 1: # At least one character has been guessed
            if move not in LETTERS: # The player entered an invalid character (such as @, #, or $)
                print('Guesses should be letters. Try again.')
                continue
            elif move in guessed: # This letter has already been guessed
                print('{} has already been guessed. Try again.'.format(move))
                continue
            elif move in VOWELS and player.prizeMoney < VOWEL_COST: # If it's a vowel, we need to be sure the player has enough prize money
                    print('Need ${} to guess a vowel. Try again.'.format(VOWEL_COST))
                    continue
            else:
                return move
        else: # The player guessed the phrase
            return move

################################################
# Create and set up players to play the game
################################################
num_human = getNumberBetween('How many human players? ', 0, 10)

# Create the human player instances
human_players = [WOFHumanPlayer(input('Enter the name for human player #{}: '.format(i+1))) for i in range(num_human)]

num_computer = getNumberBetween('How many computer players? ', 0, 10)

# If there are computer players, ask what level they should be; A level determines the skill
if num_computer >= 1:
    level = getNumberBetween('What level for the computers? (1-10) ', 1, 10)

# Create the computer player instances
computer_players = [WOFComputerPlayer('Computer {}'.format(i+1), level) for i in range(num_computer)]

players = human_players + computer_players

if len(players) == 0: # No players, no game
    print('We need players to play!')
    raise Exception('Not enough players')

################################################
# Game Logic
################################################
print('='*16)
print('WHEEL OF FORTUNE')
print('='*16)
print('')

# Category and phrase are strings
category, phrase = getRandomCategoryAndPhrase()
# Guessed is a list of the letters that have been guessed so far in the game
guessed = []

# playerIndex keeps track of the index (0 to len(players)-1) of the player whose turn it is
playerIndex = 0

# Will be set to the player instance when/if someone wins
winner = False

while True:
    player = players[playerIndex]
    wheelPrize = spinWheel()

    print('')
    print('-'*15)
    print(showBoard(category, obscurePhrase(phrase, guessed), guessed))
    print('')
    print('{} spins...'.format(player.name))
    time.sleep(2) # Pause for dramatic effect!
    print('{}!'.format(wheelPrize['text']))
    time.sleep(1) # Pause again for more dramatic effect!

    if wheelPrize['type'] == 'bankrupt':
        player.goBankrupt()
    elif wheelPrize['type'] == 'loseturn':
        pass # Do nothing; just move on to the next player
    elif wheelPrize['type'] == 'cash':
        move = requestPlayerMove(player, category, guessed)
        if move == 'EXIT': # Leave the game
            print('Until next time! Thank you for playing the game!')
            break
        elif move == 'PASS': # Move on to the next player
            print('{} passes'.format(player.name))
        elif len(move) == 1: # The player guessed a letter
            guessed.append(move)

            print('{} guesses "{}"'.format(player.name, move))

            count = phrase.count(move) # Returns an integer with how many times this letter appears
            if count > 0:
                if count == 1:
                    print("There is one {}".format(move))
                else:
                    print("There are {} {}'s".format(count, move))

                # Give the player their money and the prizes
                if move in VOWELS:
                    player.prizeMoney -= VOWEL_COST

                else:
                    player.addMoney(count * wheelPrize['value'])
                    if wheelPrize['prize']:
                        player.addPrize(wheelPrize['prize'])

                # Check if all of the letters have been guessed
                if obscurePhrase(phrase, guessed) == phrase:
                    winner = player
                    break

                continue # This player gets to go again

            else: # count == 0
                print("There is no {}".format(move))

        else: # The player guessed the whole phrase
            if move == phrase: # The player guessed the full phrase correctly
                winner = player
                # Give the player their money and the prizes
                player.addMoney(wheelPrize['value'])
                if wheelPrize['prize']:
                    player.addPrize(wheelPrize['prize'])
                break
            else:
                print('{} was not the phrase'.format(move))

    # Move on to the next player (or go back to player[0] if we reached the end)
    playerIndex = (playerIndex + 1) % len(players)

if winner:
    # Declaration of winner and results
    print('{} wins! The phrase was {}'.format(winner.name, phrase))
    print('{} won ${}'.format(winner.name, winner.prizeMoney))
    if len(winner.prizes) > 0:
        print('{} also won:'.format(winner.name))
        for prize in winner.prizes:
            print('    - {}'.format(prize))
else:
    print('Nobody won. The phrase was {}'.format(phrase))
