__author__ = 'codesse'

from functools import cmp_to_key
from random import shuffle
from time import time


class HighScoringWords:
    MAX_LEADERBOARD_LENGTH = 100  # the maximum number of items that can appear in the leaderboard
    MIN_WORD_LENGTH = 3  # words must be at least this many characters long
    letter_values = {}
    valid_words = []

    def __init__(self, validwords='wordlist.txt', lettervalues='letterValues.txt'):
        """
        Initialise the class with complete set of valid words and letter values by parsing text files containing the data
        :param validwords: a text file containing the complete set of valid words, one word per line
        :param lettervalues: a text file containing the score for each letter in the format letter:score one per line
        :return:
        """
        self.leaderboard = []  # initialise an empty leaderboard
        with open(validwords) as f:
            self.valid_words = f.read().splitlines()

            # TODO remove this line. it was for debug reasons
            # shuffle(self.valid_words)  # just to

        with open(lettervalues) as f:
            for line in f:
                (key, val) = line.split(':')
                self.letter_values[str(key).strip().lower()] = int(val)

    def build_leaderboard_for_word_list(self, valid_words=None, keep_number=100):
        """
        Build a leaderboard of the top scoring MAX_LEADERBOAD_LENGTH words from the complete set of valid words.
        :return:
        """
        words = self.valid_words if valid_words is None else valid_words
        word_d = dict([(word, sum([self.letter_values[letter] for letter in list(word)]))
                       for word in words])

        def compare_func(aa, bb):
            if aa[1] < bb[1]:
                return -1
            elif aa[1] > bb[1]:
                return 1
            else:
                # NOTE that this is in reverse because we do NOT the alphabetical order in reverse
                if aa[0] < bb[0]:
                    return 1
                elif aa[0] > bb[0]:
                    return -1
                else:
                    return 0

        sorted_words = sorted(word_d.items(), key=cmp_to_key(compare_func), reverse=True)
        high_words = sorted_words if keep_number is None else sorted_words[:keep_number]
        return [tpl[0] for tpl in high_words]

    def build_leaderboard_for_letters_version0(self, starting_letters, debug=False):
        """
        Build a leaderboard of the top scoring MAX_LEADERBOARD_LENGTH words that can be built using only the letters contained in the starting_letters String.
        The number of occurrences of a letter in the startingLetters String IS significant. If the starting letters are bulx, the word "bull" is NOT valid.
        There is only one l in the starting string but bull contains two l characters.
        Words are ordered in the leaderboard by their score (with the highest score first) and then alphabetically for words which have the same score.
        :param starting_letters: a random string of letters from which to build words that are valid against the contents of the wordlist.txt file
        :return:
        """
        start_lett_list = list(starting_letters)
        if debug:
            print(start_lett_list)
        start_lett_set = set(start_lett_list)

        words = []
        for word in self.valid_words:
            chars = list(word)

            if len(set(chars).difference(start_lett_set)) > 0:  # optimization check
                continue  # we win ~ 0.08 seconds for 'deora' case

            letters = start_lett_list[:]
            for char in chars:
                if char in letters:
                    letters.remove(char)

            will_include_word = len(starting_letters) - len(letters) == len(word)
            if will_include_word:
                words.append(word)

        return self.build_leaderboard_for_word_list(valid_words=words, keep_number=None)

    def build_leaderboard_for_letters(self, starting_letters, debug=False):
        """
        Build a leaderboard of the top scoring MAX_LEADERBOARD_LENGTH words that can be built using only the letters contained in the starting_letters String.
        The number of occurrences of a letter in the startingLetters String IS significant. If the starting letters are bulx, the word "bull" is NOT valid.
        There is only one l in the starting string but bull contains two l characters.
        Words are ordered in the leaderboard by their score (with the highest score first) and then alphabetically for words which have the same score.
        :param starting_letters: a random string of letters from which to build words that are valid against the contents of the wordlist.txt file
        :return:
        """

        # alternative idea is to build a dictionary with letter frequencies and work on that
        # Actually this improves speed about 0.07 seconds from the original above version for the deora case
        def word_to_freq(ww):
            wd = dict()
            for cc in ww:
                wd.setdefault(cc, 0)
                wd[cc] += 1
            return wd

        start_lett_list = list(starting_letters)
        start_lett_dic = word_to_freq(starting_letters)
        # print(start_lett_dic)
        # print(start_lett_list)
        start_lett_set = set(start_lett_list)

        # preprocessing step (not to be counted in seconds)
        words_dicts = [(valid_word, word_to_freq(valid_word)) for valid_word in self.valid_words]
        # print(words_dicts[:2])

        start = time()

        words = []
        for word, cur_dict in words_dicts:

            if len(set(cur_dict.keys()).difference(start_lett_set)) > 0:
                continue

            will_include_word = True
            for char, count in cur_dict.items():
                more_letters_than_offered = count > start_lett_dic[char]
                if more_letters_than_offered:
                    will_include_word = False
                    break

            if will_include_word:
                words.append(word)

        dur = time() - start
        if debug:
            print(dur)

        return self.build_leaderboard_for_word_list(valid_words=words, keep_number=None)

        # TODO next idea given more time would be to create a fully new custom solution for letters leaderboard to minimize for-loops
        #  if optimizing speed (in the expense of less organized code) would be our goal


if __name__ == '__main__':
    pass
    obj = HighScoringWords()

    # start = time()
    leaderboard = obj.build_leaderboard_for_letters('deora')
    # dur = time() - start
    # print(dur)

    print(len(leaderboard))
    print(leaderboard)
