# 6.0001 Problem Set 3 - Word game (Scrabble)

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1,
    'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """

    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    (eg. list = ['abc', '123', 'abc']
     return:  {'abc': 2, '123': 1}  // 'abc' appears twice and '123' appears once
    """

    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1  # freq.get --> looks for 'x'.  If 'x' not found, return '0'
    return freq


#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters,
    or the empty string "". You may not assume that the string will only contain
    lowercase letters, so you will have to handle uppercase and mixed case strings
    appropriately.

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    score = 0
    word = word.lower()
    for i in word:
        if i != "*":
            score += SCRABBLE_LETTER_VALUES[i]
    score_component2 = 7 * len(word) - 3 * (n - len(word))
    if score_component2 > 1:
        score *= score_component2
    else:
        score *= 1
    return score


def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """

    for letter in hand.keys():
        for j in range(hand[letter]):
            print(letter, end=' ')  # print all on the same line
    print()  # print an empty line


def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """

    hand = {}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels):
        x = random.choice(VOWELS)
        if i == 0:
            hand["*"] = hand.get("*", 0) + 1
        else:
            hand[x] = hand.get(x, 0) + 1

    for i in range(num_vowels, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand


def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured).

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)
    returns: dictionary (string -> int)
    """
    hand_copy = hand.copy()
    hand_remaining = {}
    word = word.lower()

    for key in hand:
        for letter in word:
            if letter == key:
                hand_copy[key] = hand_copy.get(key) - 1

        if hand_copy[key] > 0:
            hand_remaining[key] = hand_copy.get(key)

    return (hand_remaining)


def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.

    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    word = word.lower()
    hand_copy = hand.copy()
    for char in word:
        if char not in hand:
            return False
        else:
            hand_copy[char] = hand_copy.get(char) - 1
            if hand_copy[char] < 0:
                return False
    if word in word_list:
        return True
    elif "*" not in word:
        return False
    else:
        for vowel in "aeiou":
            test_word = word.replace("*", vowel)
            if test_word in word_list:
                return True
    return False


def calculate_handlen(hand):
    """
    Returns the length (number of letters) in the current hand.

    hand: dictionary (string-> int)
    returns: integer
    """

    length = 0
    for char in hand:
        length += hand.get(char)
    return length


def play_hand(hand, word_list):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.

    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand

    """

    # Keep track of the total score
    score = 0

    # As long as there are still letters left in the hand:
    while calculate_handlen(hand) > 0:

        # Display the hand
        print("Current hand: ", end='')
        display_hand(hand)

        # Ask user for input
        word = input("Enter word, or \"!!\" to indicate that you are finished: ")

        # If the input is two exclamation points:
        if word == "!!":
            # End the game (break out of the loop)
            break

        # Otherwise (the input is not two exclamation points):
        else:
            # If the word is valid:
            if is_valid_word(word, hand, word_list):
                # Tell the user how many points the word earned, and the updated total score
                word_score = get_word_score(word, calculate_handlen(hand))
                score += word_score
                print("\"" + word + "\" earned", word_score, "points. Total: ", score, "\n")

            # Otherwise (the word is not valid):
            else:
                # Reject invalid word (print a message)
                print("This is not a valid word.  Please choose another word. \n")
            # update the user's hand by removing the letters of their inputted word
            hand = update_hand(hand, word)

    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score
    if calculate_handlen(hand) == 0:
        print("Ran out of letters")

    # Return the total score as result of function
    return (score)



#
# procedure you will use to substitute a letter in a hand
#

def substitute_hand(hand, letter):
    """
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.

    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """
    # creates new_hand that is returned to user (original hand is not mutated)
    new_hand = hand.copy()

    # If "letter" is found in hand
    if letter in hand:
        num_letter = hand[letter]

        # obtain new letter to replace letter to be deleted
        new_letter = letter
        while new_letter in hand:
            new_letter = random.choice(VOWELS + CONSONANTS)

        # Delete all copies of the letter
        del (new_hand[letter])

        # Add new letter to replace letter deleted
        new_hand[new_letter] = num_letter

        # return new hand
        return (new_hand)

    # Else if "letter" not found in hand
    else:
        # return original hand
        return (hand)


def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the
      entire series

    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep
      the better of the two scores for that hand.  This can only be done once
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.

    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """

    num_hands = int(input("Enter total number of hands: "))
    hand = deal_hand(HAND_SIZE)
    score_total = 0

    while num_hands > 0:
        print("Current hand: ", end='')
        display_hand(hand)

        # substitute letter in hand
        substitute = input("\nWould you like to substitute a letter? ")
        substitute = substitute.lower()
        if substitute == "yes":
            letter = input("Which letter would you like to replace: ")
            print("")
            hand = substitute_hand(hand, letter)

        # play game and prints score for current game
        score = play_hand(hand, word_list)
        score_total += score
        print("Total score for this hand: ", score, "\n----------")

        num_hands -= 1
        if num_hands == 0:
            break

        replay = input("Would you like to replay the hand? ")
        replay = replay.lower()

        if replay == "no":
            hand = deal_hand(HAND_SIZE)
    print("Total score over all hands: ", score_total)


#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)


