import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist


def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'


class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object

        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text = text
        self.valid_words = load_words("words.txt")

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class

        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.

        Returns: a COPY of self.valid_words
        '''
        copy_valid_words = self.valid_words[:]
        return copy_valid_words

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.

        shift (integer): the amount by which to shift every letter of the
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        '''
        shift_dict = {}

        i = 0
        for char in string.ascii_lowercase:
            # Adds lowercase letters to dictionary and its corresponding shift
            shift_dict[char] = string.ascii_lowercase[(i + shift) % 26]
            i += 1

        # Creates a copy of shift_dict to iterate over so dict does not change size during iteration
        shift_dict_copy = shift_dict.copy()

        for key in shift_dict_copy:
            # Converts lowercase to uppercase.  Adds a copy of uppercase letters and its
            # corresponding shift to dictionary
            uppercase_key = key.upper()
            uppercase_value = shift_dict_copy[key].upper()
            shift_dict[uppercase_key] = uppercase_value
        return shift_dict

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift

        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift.  Puntuations and spaces are not
             changed.
        '''
        shift_message = ""
        shift_dict = self.build_shift_dict(shift)

        for char in self.message_text:
            if char in shift_dict:
                shift_char = shift_dict[char]
            else:
                shift_char = char
            shift_message += shift_char

        return shift_message


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object

        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(self.shift)
        self.message_text_encrypted = self.apply_shift(self.shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class

        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class

        Returns: a COPY of self.encryption_dict
        '''
        encryption_dict_copy = self.encryption_dict.copy()
        return encryption_dict_copy

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class

        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other
        attributes determined by shift.

        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(self.shift)  # reinitializes encryption dict
        self.message_text_encrypted = self.apply_shift(self.shift)  # reinitializes message text encrypted


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object

        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create
        the maximum number of valid words, you may choose any of those shifts
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        shift = 0

        # list that stores [shift : num of valid words]
        list_shift_validwords = []

        while shift <= 26:
            shift_dict = self.build_shift_dict(shift)

            # apply shift to decode message
            shift_message = self.apply_shift(shift)

            # checks if each word in message is a valid word
            shift_message_wordlist = shift_message.split()  # returns a list of words in shift_message (eg. ['Hello', 'world'])
            valid_words = 0
            for word in shift_message_wordlist:
                if is_word(self.valid_words, word):
                    valid_words += 1
                list_shift_validwords.append([shift, valid_words])

            shift += 1

        # returns tuple of best shift value + decrypted message using that shift (eg. (3, "Hello"))
        shift, valid_word = max(list_shift_validwords,
                                key=lambda item: item[1])  # finds pair with the max value for valid_words
        best_shift_tuple = (shift, self.apply_shift(shift))
        return best_shift_tuple


if __name__ == '__main__':
    # Example test case 1 (PlaintextMessage)
    print("Example test case 1: PlaintextMessage")
    plaintext = PlaintextMessage('hello', 2)
    print('Expected Output: jgnnq')
    print('Actual Output:', plaintext.get_message_text_encrypted())

    # Example test case 2 (PlaintextMessage)
    print("\n Example test case 2: PlaintextMessage")
    plaintext2 = PlaintextMessage('This is a test.', 4)
    print('Expected Output: Xlmw mw e xiwx.')
    print('Actual Output:', plaintext2.get_message_text_encrypted())

    # Example test case 1 (CiphertextMessage)
    print("\n Example test case 3: CiphertextMessage")
    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())

    # Example test case 2 (CiphertextMessage)
    print("\n Example test case 4: CiphertextMessage")
    ciphertext2 = CiphertextMessage('Xlmw mw e xiwx.')
    print('Expected Output:', (22, 'This is a test.'))
    print('Actual Output:', ciphertext2.decrypt_message())

    # Problem set part 4:  Loads "story.txt" (encrypted message) as a string and decrypts it
    print("\n Problem set part 4:  Decrypt story.txt")
    story_encrypted = get_story_string()
    story = CiphertextMessage(story_encrypted)
    print(story.decrypt_message())
