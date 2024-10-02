################################################
# Title     : Wordle Game
# Author    : balarcode
# Version   : 1.0
# Date      : 2nd October 2024
# File Type : Python Script / Program
# File Test : Verified on Python 3.12.6
# Comments  : Game rules are provided below.
#             1) Each guess must be a five letter English word. Only the 26 letters of the English alphabet are used and case does not matter.
#             2) The game engine generates a hidden 5 letter word called the target word.
#             3) The bot plays the game and attempts to guess the word. It will get up to six tries.
#             4) The bot will be given the location of a datafile which has a list of allowable words (one per line). Bot can only make guesses from this datafile.
#             5) After each guess, the game engine provides feedback indicating if each character was in the correct position for the target word, and if not, if the character is in the target word but in the wrong position.
#             6) The bot must be smart such that once it has identified the correct position of a letter in a word it must only guess future words where that letter is in the same position.
#
# All Rights Reserved.
################################################

import random
import os

# NOTE: Use the below code snippet to figure out the absolute path to the working directory.
#       Failure to do so will lead to program failure while reading files.
cwd = os.getcwd() # Get the current working directory
files = os.listdir(cwd) # Get all the files and sub-directories in that directory
print("Files in {}: {}".format(cwd, files))
working_directory = cwd + "/Python/wordle/"
print("Working directory is: {}".format(working_directory))

################################################
# Class Definitions
################################################
# Class to handle a single English letter from a guessed word
class Letter:
    """Class to handle a single English letter from a guessed word."""
    in_correct_place: bool = False
    in_word: bool = False
    def __init__(self, letter: str) -> None:
        self.letter: str = letter
    def is_in_correct_place(self) -> bool:
        return self.in_correct_place
    def is_in_word(self) -> bool:
        return self.in_word

# Class to represent a Bot which is a game playing agent
class Bot:
    """Class to represent a Bot which is a game playing agent."""
    word_list: list[str] = []
    def __init__(self, word_list_file: str) -> None:
        self.word_list: list(str) = list( map(lambda x: x.strip().upper(), open(word_list_file, "r").readlines()) )
        self.past_guesses = []
        self.correctly_guessed_letters_in_place = {}
        self.unused_letters = []
        self.invalid_guess = False

    def make_guess(self) -> str:
        """Ensure that make_guess() returns a smartly guessed word by the Bot."""
        self.invalid_guess = False
        counter = 1
        while (True):
            random_guess = random.choice(self.word_list).upper()
            if random_guess not in self.past_guesses:
                self.past_guesses.append(random_guess)
                self.invalid_guess = False
                # Check if the newly guessed word has unused letters; If yes, then guess a new random word
                for j in range(len(random_guess)):
                    if random_guess[j] in self.unused_letters:
                        self.invalid_guess = True
                # Check if the newly guessed word has the letters at correctly guessed position from previous tries
                ks = list(self.correctly_guessed_letters_in_place.keys())
                for j in range(len(random_guess)):
                    if len(ks) != 0:
                        if self.correctly_guessed_letters_in_place[ks[j]] != None:
                            if (random_guess[j] != self.correctly_guessed_letters_in_place[ks[j]]):
                                self.invalid_guess = True
            else:
                self.invalid_guess = True
            counter += 1
            if self.invalid_guess == False:
                break # Break the while-loop once a valid guess is found by the Bot
        print("Guessed word by the Bot: {}\n\n".format(random_guess))
        return random_guess

    def record_guess_results(self, guess: str, guess_results: list[Letter]) -> None:
        """Store the metadata for the guessed word."""
        for j in range(len(guess)):
            if guess_results[j].in_correct_place:
                self.correctly_guessed_letters_in_place[j] = guess[j]
            else:
                self.correctly_guessed_letters_in_place[j] = None
            if guess_results[j].in_word == False:
                self.unused_letters.append(guess[j])

# Class to play the Wordle game
class GameEngine:
    """The GameEngine represents a new Wordle game for play."""
    def __init__(self):
        self.err_input = False
        self.err_guess = False
        self.prev_guesses = []

    def play(self, bot, word_list_file: str = "words.txt", target_word: str = None) -> None:
        """Play a new game using the supplied bot. By default the GameEngine
        will look in words.txt for the list of allowable words and choose one
        at random. Set the value of target_word to override this behavior and
        choose the word that must be guessed by the bot.
        """
        def format_results(results) -> str:
            """Function to format the results into a string for quick review by the caller."""
            response = ""
            for letter in results:
                if letter.is_in_correct_place():
                    response = response + letter.letter
                elif letter.is_in_word():
                    response = response + "*"
                else:
                    response = response + "?"
            return response

        def set_feedback(guess: str, target_word: str) -> tuple[bool, list[Letter]]:
            """Return the results of a guessed word as a tuple."""
            # Whether the complete guess is correct or not,
            # set it to True initially and then switch it to False if any letter doesn't match
            correct: bool = True
            letters = []
            for j in range(len(guess)):
                # Create a new Letter object
                letter = Letter(guess[j])
                # Check to see if this character is in the same position in the
                # guessed word and if so, set the in_correct_place attribute
                if guess[j] == target_word[j]:
                    letter.in_correct_place = True
                    known_letters[j] = guess[j]  # Record the known correct positions
                else:
                    # The bot doesn't have a perfect answer, so update
                    # the correct flag for feedback
                    correct = False
                # Check to see if this character is anywhere in the target word
                if guess[j] in target_word:
                    letter.in_word = True
                else:
                    unused_letters.add(guess[j])  # Record the unused letters
                # Add this letter object to the list of Letters
                letters.append(letter)
            return correct, letters

        # Read in the dictionary of allowable words
        word_list: list(str) = list(map(lambda x: x.strip().upper(), open(word_list_file, "r").readlines()))
        # Initialize the known correct positions
        known_letters: list(str) = [None, None, None, None, None]
        # Initialize the set of unused letters
        unused_letters = set()

        # Assign the target word to a member variable for use later
        if target_word is None:
            target_word = random.choice(word_list).upper()
        else:
            target_word = target_word.upper()
            if target_word not in word_list:
                print(f"Target word {target_word} must be from the word list!")
                self.err_input = True
                return

        print(f"Playing a game of Wordle using the word list file of {word_list_file}.\nThe target word for this round is {target_word}\n")

        MAX_GUESSES = 6 # Only six tries are allowed for the bot playing agent
        for i in range(1, MAX_GUESSES):
            # Ask the bot for its guess and evaluate
            guess: str = bot.make_guess()
            # Print out a line indicating what the guessed word was
            print(f"Evaluating bot guess of {guess}")
            if guess not in word_list:
                print(f"Guessed word {guess} must be from the word list!")
                self.err_guess = True
            elif guess in self.prev_guesses:
                print(f"Guess word cannot be the same one as previously used!")
                self.err_guess = True
            if self.err_guess:
                return

            self.prev_guesses.append(guess)  # Record the previous guess

            for j, letter in enumerate(guess):
                if letter in unused_letters:
                    print(
                        f"The bot's guess used {letter} which was previously identified as not used!"
                    )
                    self.err_guess = True
                if known_letters[j] is not None:
                    if letter != known_letters[j]:
                        print(
                            f"Previously identified {known_letters[j]} in the correct position is not used at position {j}!"
                        )
                        self.err_guess = True
                if self.err_guess:
                    return

            # Get the results of the guess
            correct, results = set_feedback(guess, target_word)
            # Print out a line indicating whether the guess was correct or not
            print(f"Was this guess correct? {correct}")
            # Send the guess results to Bot
            print(f"Sending guess results to bot {format_results(results)}\n")
            bot.record_guess_results(guess, results)
            # If the guessed word is correct, then we can just end the game
            if correct:
                print(f"Great job, Bot found the target word in {i} guesses!")
                return

        # If we get here, the Bot didn't guess the word
        print(f"Thanks for playing! Bot didn't find the target word in the number of guesses allowed.")
        return

################################################
# Game Logic
################################################
print('='*8)
print(' WORDLE ')
print('='*8)
print('')

words_file = working_directory + "words.txt"

# Initialize the Bot which plays the game
bot = Bot(words_file)

# Create a new GameEngine and play a game with the Bot
GameEngine().play(bot, word_list_file=words_file)
