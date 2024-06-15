"""
Provides functions to split Czech words into syllables based on Czech language rules.

- count_syllables(word: str) -> int: Returns the number of syllables in the given word.
- split_to_characters(word: str) -> list[str]: Splits the word into individual characters,
  collapsing subsequent 'c' and 'h' into one character ('ch')
- split_to_syllables(word: str) -> list[str]: Splits the word into syllables

Usage example:
    word = "příklad"
    syllables = split_to_syllables(word)
    print(syllables)  # Output: ['pří', 'klad']
"""

LETTER_GROUPS = [
    'stř', 'tr', 'vr', 'stv', 'sk', 'st', 'pr', 'sl', 'tř', 'šm', 'pl', 'br', 'kl', 'kr', 'bl', 'sv', 'hl'
]

def count_syllables(word: str) -> int:
    """
    Count the number of czech syllables in a given word
    """
    return len(split_to_syllables(word))

def split_to_characters(word: str) -> list[str]:
    """
    Split the word into individual characters, respecting czech 'ch' character
    """
    word_letters = list(word.lower())
    # collapse subsequent 'c' and 'h' into one character
    word_chars = []
    was_ch = False
    for i, char in enumerate(word_letters):
        if char in ['c', 'C'] and i < len(word_letters) - 1 and word_letters[i + 1] in ['h', 'H']:
            word_chars.append(char + word_letters[i + 1])
            was_ch = True
        elif was_ch:
            was_ch = False
            continue
        else:
            word_chars.append(char)
    return word_chars

def split_to_syllables(word: str) -> list[str]:
    """
    Split the word into syllables
    """
    word_chars = split_to_characters(word)

    vowels = set("aeiuoyáéíóúůýěäëïöü")

    syllable_indexes: list[list[int]] = []
    # iterate and find the vowels
    previous_char = None
    for index, char in enumerate(word_chars):
        next_char = word_chars[index + 1] if index + 1 < len(word_chars) else None
        if (char == 'u') and ((index == 1 and previous_char in ['a', 'e']) or \
                              previous_char == 'o'):
            # Add the u to the previous syllable ~ handles the (^eu|^au|ou) cases
            syllable_indexes[-1][1] = index
        elif char in vowels or (char in ['r', 'l'] and previous_char not in vowels and next_char not in vowels):
            # creates new syllable
            syllable_indexes.append([index, index])

        previous_char = char

    # Edge case: if there were no vowels in the word
    if len(syllable_indexes) <= 0:
        return [word]

    # expand the syllables on the edges
    syllable_indexes[0][0] = 0
    syllable_indexes[-1][1] = len(word_chars) - 1

    expand_syllables_from_left(syllable_indexes, word_chars)

    # Expand the syllables from right:
    for i in range(0, len(syllable_indexes) - 1):
        # expand to the right
        if i == 0 and 'ne' == ''.join(word_chars[syllable_indexes[i][0]: syllable_indexes[i][1] + 1]) and \
                'nerv' != ''.join(word_chars[syllable_indexes[i][0]: syllable_indexes[i][1] + 3]):
            # expand to the left instead
            syllable_indexes[i + 1][0] = syllable_indexes[i][1] + 1
        else:
            syllable_indexes[i][1] = syllable_indexes[i + 1][0] - 1

    # Handle case based on the original
    lowercase_syllables = [''.join(word_chars[start:end + 1]) for start, end in syllable_indexes]
    truecase_syllables = []
    i = 0
    for lowercase_syllable in lowercase_syllables:
        truecase_syllables.append(word[i:i + len(lowercase_syllable)])
        i += len(lowercase_syllable)
    return truecase_syllables

def expand_syllables_from_left(syllable_indexes: list[list[int]], word_chars: list[str]) -> None:
    """
    A helper function for the syllable splitting
    """
    for i in range(1, len(syllable_indexes)):
        # expand to left by one unless already used by the previous syllable
        if syllable_indexes[i - 1][1] < syllable_indexes[i][0] - 1:
            syllable_indexes[i][0] = syllable_indexes[i][0] - 1
        for letter_group in LETTER_GROUPS:
            left_index = syllable_indexes[i][0] + 1
            if ''.join(word_chars[left_index - len(letter_group): left_index]) == letter_group:
                syllable_indexes[i][0] = left_index - len(letter_group)
                if syllable_indexes[i - 1][1] > syllable_indexes[i][0]:
                    syllable_indexes[i - 1][1] = syllable_indexes[i][0] - 1
                break
