# Problem Set 2 - Hangman Game

import random
import string

WORDLIST_FILENAME = "words.txt"  #Text file containing a list of legitimate words


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)




# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    
    x=0   #Number of letters that have been guessed correctly
    for char in secret_word:
        for letter in letters_guessed:
            if letter == char:
                x+=1
                break  #avoids re-running for... loop once letter matches char. 
                       #Also prevents multiple guesses of same letter to increase counter once the char has been guessed
    return x==len(secret_word)


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''

    guessed_word = ""
    for char in secret_word:
        if char in letters_guessed:
            guessed_word += char
        else:
            guessed_word += "_ "
    return guessed_word





def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''

    avail_letter_array = list(filter(lambda x : not x in letters_guessed, string.ascii_lowercase))
    return(''.join(avail_letter_array))


def subtract_warning(warnings_remaining, guesses_remaining):
    '''
    Use to subtract number of warnings remaining.  If warnings = 0, one guess is subtracted instead.
    '''
    if warnings_remaining > 0:
        warnings_remaining -= 1
        print("You have ", warnings_remaining, "warnings left.")
        return (warnings_remaining, guesses_remaining)
    elif guesses_remaining > 0:
        guesses_remaining -= 1
        print("You have no warnings left, so you lose one guess.")
        return (warnings_remaining, guesses_remaining)
    else:
        return(0,0)
    
def unique_letters_in_word(secret_word):
    '''
    Returns number of unique letters in secret_word (eg."Hello" = 4)
    Used to calculate points at the end of Hangman game
    '''
    
    letters = []
    unique_letters_count = 0
    for char in secret_word:
        if char not in letters:
            unique_letters_count += 1
        letters += char
    return(unique_letters_count)


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    
    warnings_remaining = 3   #User start with 3 warnings
    guesses_remaining = 6   #User start with 6 guesses
    letters_guessed = []
    score = 0
    print("Welcome to the game Hangman!\nI am thinking of a word that is", len(secret_word), "letters long.")
    print("-----------------------------------")
    
    while guesses_remaining > 0 and is_word_guessed(secret_word, letters_guessed) == False:
        print("You have ", guesses_remaining, "guesses left.")
        print("Available letters: ", get_available_letters(letters_guessed))
        guess = input("Please guess a letter: ")
        guess = guess.lower()  # converts user input to lowercase

        if guess in letters_guessed:
            print("Opps!  You've already guessed that letter.")
            [warnings_remaining, guesses_remaining] = subtract_warning(warnings_remaining, guesses_remaining)
        elif guess in secret_word:
            letters_guessed += guess
            print("Good guess: ")
        elif not guess in string.ascii_lowercase:
            print("Opps! That is not a valid letter.")
            [warnings_remaining, guesses_remaining] = subtract_warning(warnings_remaining, guesses_remaining)
        else:
            print("Opps!  That letter is not in my word.")
            letters_guessed += guess
            if guess in ['a','e','i','o','u']:
                guesses_remaining -= 2
            else:
                guesses_remaining -= 1
        print(get_guessed_word(secret_word, letters_guessed))
        print("-----------------------------------")
    
    if is_word_guessed(secret_word, letters_guessed) == True:
        score = guesses_remaining * unique_letters_in_word(secret_word)
        print("Congratulations, you won! \nYour total score for this game is :", score)
    else:
        print("Sorry, you ran out of guesses.  The word was:", secret_word + ".")



# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word_nospace = my_word.replace(" ","")
    
    if len(my_word_nospace) != len(other_word):
        return False
    
    i = 0  #counter for letter position in other_word
    
    for char in my_word_nospace:
        if char == "_" and other_word[i] in my_word_nospace: #if the secret character has already been guessed (eg. a_ple, apple --> false)
            return False
        if char != other_word[i] and char != "_": #if secret char is an alphabet and doesn't match guessed character
            return False
        i+=1
    return True


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    matches = [] #words from wordlist that matches my_word
    my_word = my_word.replace(" ","") #Removes spaces in my_word
    
    #Only words from wordlist that match length of my_word will go through function match_with_gaps
    wordlist_right_length = list(filter(lambda x: len(my_word) == len(x), wordlist))
    
    for wordlist_word in wordlist_right_length:
        if match_with_gaps(my_word, wordlist_word):
            matches.append(wordlist_word)
    if 0 == len(matches):
        print("No matches found")
    else:
        print(matches)


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
  
    warnings_remaining = 3   #User start with 3 warnings
    guesses_remaining = 6   #User start with 6 guesses
    letters_guessed = []
    score = 0

    print("Welcome to the game Hangman!\nI am thinking of a word that is", len(secret_word), "letters long.")
    print("-----------------------------------")
    
    while guesses_remaining > 0 and not is_word_guessed(secret_word, letters_guessed):
        print("You have ", guesses_remaining, "guesses left.")
        print("Available letters: ", get_available_letters(letters_guessed))
        guess = input("Please guess a letter: ")
        guess = guess.lower()  # converts user input to lowercase
        
        if len(guess) > 1:
            if guess == secret_word:
                letters_guessed = guess
                break
            else:
                print("Opps!  That is not the secret word.")
                guesses_remaining -= 1

        elif guess in letters_guessed:
            print("Opps!  You've already guessed that letter.")
            [warnings_remaining, guesses_remaining] = subtract_warning(warnings_remaining, guesses_remaining)

        elif guess in secret_word:
            letters_guessed += guess
            print("Good guess: ")

        elif guess == "*":
            show_possible_matches(get_guessed_word(secret_word, letters_guessed))

        elif not guess in string.ascii_lowercase:
            print("Opps! That is not a valid letter.")
            [warnings_remaining, guesses_remaining] = subtract_warning(warnings_remaining, guesses_remaining)

        else:
            print("Opps!  That letter is not in my word.")
            letters_guessed += guess
            if guess in ['a','e','i','o','u']:
                guesses_remaining -= 2
            else:
                guesses_remaining -= 1

        print(get_guessed_word(secret_word, letters_guessed))
        print("-----------------------------------")
    
    if is_word_guessed(secret_word, letters_guessed):
        score = guesses_remaining * unique_letters_in_word(secret_word)
        print("Congratulations, you won! \nYour total score for this game is :", score)
    else:
        print("Sorry, you ran out of guesses.  The word was:", secret_word + ".")



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.

if __name__ == "__main__":
    # pass
    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)


###############
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 

    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
