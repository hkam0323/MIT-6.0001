##################################################################################
# Will need to rename code from Problem set 4a to "ps4a.py" and place in the same
# folder for this code to run correctly
##################################################################################

import string
from ps4a import get_permutations


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


### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

# you may find these constants helpful
VOWELS_LOWER = 'aeiou'
VOWELS_UPPER = 'AEIOU'
CONSONANTS_LOWER = 'bcdfghjklmnpqrstvwxyz'
CONSONANTS_UPPER = 'BCDFGHJKLMNPQRSTVWXYZ'


class SubMessage(object):
    def __init__(self, text):
        '''
        Initializes a SubMessage object

        text (string): the message's text

        A SubMessage object has two attributes:
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
        valid_words_copy = self.valid_words[:]
        return valid_words_copy

    def build_transpose_dict(self, vowels_permutation):
        '''
        vowels_permutation (string): a string containing a permutation of vowels (a, e, i, o, u)

        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to an
        uppercase and lowercase letter, respectively. Vowels are shuffled
        according to vowels_permutation. The first letter in vowels_permutation
        corresponds to a, the second to e, and so on in the order a, e, i, o, u.
        The consonants remain the same. The dictionary should have 52
        keys of all the uppercase letters and all the lowercase letters.

        Example: When input "eaiuo":
        Mapping is a->e, e->a, i->i, o->u, u->o
        and "Hello World!" maps to "Hallu Wurld!"

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        '''

        dict_vowel_permutation = {}
        vowels_permutation = vowels_permutation.lower()
        i = 0  # counter for vowel in vowel_permutation

        # Adds lowercase keys to dict
        for char in string.ascii_lowercase:
            if char in "aeiou":
                vowel = vowels_permutation[i]
                dict_vowel_permutation[char] = vowel
                i += 1
            else:
                dict_vowel_permutation[char] = char

        # Adds uppercase keys to dict (by converting lowercase keys to uppercase)
        dict_vowel_permutation_copy = dict_vowel_permutation.copy()
        for key in dict_vowel_permutation_copy:
            dict_vowel_permutation[key.upper()] = (dict_vowel_permutation[key]).upper()

        return dict_vowel_permutation

    def apply_transpose(self, transpose_dict):
        '''
        transpose_dict (dict): a transpose dictionary

        Returns: an encrypted version of the message text, based
        on the dictionary
        '''
        encrypted_text = ""

        for char in self.message_text:
            if char in string.ascii_letters:
                encrypted_text += transpose_dict[char]
            else:
                encrypted_text += char

        return encrypted_text


class EncryptedSubMessage(SubMessage):
    def __init__(self, text):
        '''
        Initializes an EncryptedSubMessage object

        text (string): the encrypted message text

        An EncryptedSubMessage object inherits from SubMessage and has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        SubMessage.__init__(self, text)

    def decrypt_message(self):
        '''
        Attempt to decrypt the encrypted message

        Idea is to go through each permutation of the vowels and test it
        on the encrypted message. For each permutation, check how many
        words in the decrypted text are valid English words, and return
        the decrypted message with the most English words.

        If no good permutations are found (i.e. no permutations result in
        at least 1 valid word), return the original string. If there are
        multiple permutations that yield the maximum number of words, return any
        one of them.

        Returns: the best decrypted message as a string

        Hint: use your function from Part 4A
        '''
        vowel_permutations = get_permutations("aeiou")

        # List that stores ["permutation", num_valid_words]
        list_validwords = []

        # Finds list of ["permutation", num_valid_words]
        for permutation in vowel_permutations:
            transpose_dict = self.build_transpose_dict(permutation)
            decrypted_string = self.apply_transpose(transpose_dict)

            # Returns list with each word as a separate string

            decrypted_string_wordlist = decrypted_string.split()

            # Calculates number of valid words in decrypted string
            num_valid_words = 0
            for word in decrypted_string_wordlist:
                if is_word(self.valid_words, word):
                    num_valid_words += 1

            list_validwords.append([permutation, num_valid_words])

        # Finds key (permutation) with the largest value (num_valid_words) and
        # returns the decrypted message
        key, value = max(list_validwords, key=lambda x: x[1])  # key = correct permutation
        transpose_dict = self.build_transpose_dict(key)
        return self.apply_transpose(transpose_dict)


if __name__ == '__main__':
    # Example test case
    message = SubMessage("Hello World!")
    permutation = "eaiuo"
    enc_dict = message.build_transpose_dict(permutation)
    print("Original message:", message.get_message_text(), "Permutation:", permutation)
    print("Expected encryption:", "Hallu Wurld!")
    print("Actual encryption:", message.apply_transpose(enc_dict))
    enc_message = EncryptedSubMessage(message.apply_transpose(enc_dict))
    print("Decrypted message:", enc_message.decrypt_message())

    # Test case 2
    print("\n \nTest Case 2")
    message2 = SubMessage("This is a test.")
    permutation2 = "oeaiu"
    enc_dict2 = message2.build_transpose_dict(permutation2)
    print("Original message: ", message2.get_message_text(), "Permutation: ", permutation2)
    print("Expected encryption: Thas as o test.")
    print("Actual encryption: ", message2.apply_transpose(enc_dict2))
    enc_message2 = EncryptedSubMessage(message2.apply_transpose(enc_dict2))
    print("Decrypted message:", enc_message2.decrypt_message())
