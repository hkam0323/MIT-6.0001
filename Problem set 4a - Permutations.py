def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    # List of possible permutations
    permutation = []

    # Base case:  If only 1 char, return itself (permutation of 1 char is 1 char)
    if len(sequence) == 1:
        return ([sequence])

    # Recursive case: Find all the different ways to insert first character into
    # each permutation of remaining characters
    else:
        first_char = sequence[0]
        remaining_char = sequence[1:]

        remaining_char_permutations = get_permutations(remaining_char)

        # Adds first_char into remaining_char_permutations
        for r in remaining_char_permutations:  # r = bc, cb

            # Adds first_char to first and last position of remaining_char_permutations
            permutation.append(first_char + r)  # a, bc
            permutation.append(r + first_char)  # bc, a

            # Adds first_char to all other positions in remaining_char_permutations
            for i in range(1, len(r)):  # eg. bcd = len 3 --> i = 1, 2
                add_permutation = ""
                add_permutation += r[0:i] + first_char + r[i:]
                permutation.append(add_permutation)

        return (permutation)


if __name__ == '__main__':
    example_input = 'abc'
    print('Input:', example_input)
    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    print('Actual Output:', get_permutations(example_input))
