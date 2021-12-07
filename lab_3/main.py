"""
Lab 3
Language classification using n-grams
"""
# print(list(map(int, input('?').split(' '))))
import json
from typing import Dict, Tuple
import re


def tokenize_by_sentence(text: str) -> tuple:
    if not isinstance(text,str)or not text:
        return()
    UnlautsReplacements = {
        'ö': 'oe',
        'ü': 'ue',
        'ä': 'ae',
        'ß': 'ss',
        'Ö': 'Oe',
        'Ü': 'Ue',
        'Ä': 'Ae',
        'ß': 'ss',
        'ẞ': 'Ss'

    }

    def normalize(a):

        a = a.strip()
        a = re.sub(r"[^A-Za-z0-9\s]{1,}", '', a)
        for x, y in UnlautsReplacements.items():
            a = a.replace(x, y)
        return a


    text = text.replace('\r\n', ' ')
    text = text.replace('\n', ' ')
    text = text.replace('\t', ' ')
    # Break Sentences properly
    alltextstr = (text)  # list(map(normalize, f.readlines()))
    print('alltextstr', alltextstr)
    sentences = re.split(r"[!.?]\W(?=[\wöüäßÜÖÄẞ])", alltextstr)

    sentences = re.split(r"[.!?]{1,3}[\s]{1,}(?=[\wßÜÖÄ^a-z^öüäß]{1})",
                         alltextstr)  # re.split(r"[!.?]\W(?=[\wöüäßÜÖÄẞ])", text)
    print('sentences', sentences)
    sentences = list(map(normalize, sentences))

    # Lexemizations
    i = 0
    TkSentences = []
    for sent in sentences:

        print(i, ')', sent + '')
        i += 1
        tkSent = re.split(r'[\s]{1,}', sent)
        tkSent2 = []
        for word in tkSent:
            # print('\t<',word,'>',sep='', end='    =    ')
            if word == '':
                continue
            word = word.lower()
            clearword = [symb for symb in word if symb.isalpha()]

            clearword.append('_')
            clearword.insert(0, '_')
            clearword = tuple(clearword)
            # print('\t<',clearword,'>',sep='')
            tkSent2.append(clearword)

        if len(tkSent2) == 0:
            continue
        TkSentences.append(tuple(tkSent2))

    '''
    #output
    i=0
    outstr = ''
    for sent in TkSentences:
        outstr+= str(i) + ')' + str(sent) +'\n'
        for word in sent:
            outstr+= '\t' + str(word)+ '\n'
        i+=1

    print(outstr)
    '''
    return tuple(TkSentences)



class LetterStorage:

    def __init__(self):
        self.uid = 0
        # self.storage = {'errors':0}
        self.storage = {}
        self.errors = 0

    def e(self, txt):
        self.errors += 1
        print('ERROR #', self.errors, txt)
        return self.errors

    def _put_letter(self, letter: str) -> int:
        if not type(letter) is str:
            self.e('_put_letter')
            print(letter)
            return -1

        if letter not in self.storage:
            self.storage[letter] = self.uid
            self.uid += 1
            return 0

        return self.storage[letter]

    def get_id_by_letter(self, letter):
         """
        Gets a unique id by a letter
        :param letter: a letter
        :return: an id
        """
         if letter in self.storage:
            return self.storage[letter]
         else:
            return -1

    def get_letter_by_id(self, letter_id: int) -> str or int:
        """
        Gets a letter by a unique id
        :param letter_id: a unique id
        :return: letter
        """
        if not isinstance(letter_id, int) \
                or letter_id not in self.storage.values():
            return -1
        for letter, id_letter in self.storage.items():
            if id_letter == letter_id:
                return letter
            

    def update(self, corpus):
        ss = corpus
        if type(ss) is not tuple:
            self.e('update')
            return -1

        uniques = {}
        for sent in ss:
            for word in sent:
                for letter in word:

                    if self._put_letter(letter) == -1:
                        return -1

        return 0


# class STORAGE ENDS
# ========================



def encode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    if not (isinstance(storage, LetterStorage) and isinstance(corpus, tuple)):
        return ()
    # >no need in storage.update(corpus)
    encoded_sentences = tuple(tuple(tuple(storage.get_id_by_letter(letter)
                                          for letter in word)
                                    for word in sentence)
                              for sentence in corpus)

    return encoded_sentences


def decode_corpus(storage: LetterStorage, corpus: tuple) -> tuple:
    """
    Decodes sentences by replacing letters with their ids
    :param storage: an instance of the LetterStorage class
    :param corpus: an encoded tuple of sentences
    :return: a tuple of the decoded sentences
    """
    if not (isinstance(storage, LetterStorage) and isinstance(corpus, tuple)):
        return ()
    # >no need in storage.update(corpus)
    decoded_sentences = tuple(tuple(tuple(storage.get_letter_by_id(letter)
                                          for letter in word)
                                    for word in sentence)
                              for sentence in corpus)
    return decoded_sentences

    pass



class NGramTrie:
    """
        ngrams logic maintainer
    """

    def __init__(self, n: int, letter_storage: LetterStorage):
        self.size = n
        self.storage = letter_storage
        self.n_grams = []
        self.n_gram_frequencies = {}
        self.n_gram_log_probabilities = {}

    # 6 - biGrams
    # 8 - threeGrams
    # 10 - nGrams
    def extract_n_grams(self, encoded_corpus: tuple) -> int:
        """
        Extracts n-grams from the given sentence, fills the field n_grams
        :return: 0 if succeeds, 1 if not
        e.g.
        encoded_corpus = (
            ((1, 2, 3, 4, 1), (1, 5, 2, 1)),
            ((1, 3, 4, 1), (1, 5, 2, 1))
        )
        self.size = 2
        --> (
            (
                ((1, 2), (2, 3), (3, 4), (4, 1)), ((1, 5), (5, 2), (2, 1))),
                (((1, 3), (3, 4), (4, 1)), ((1, 5), (5, 2), (2, 1))
            )
        )
        """
        if not isinstance(encoded_corpus, tuple):
            return 1
        siz = self.size - 1  # usual string length compenstaion =)
        n_grams = tuple(tuple(tuple(word[i - siz:i]
                                    for i in range(siz, len(word)))
                              for word in sent)
                        for sent in encoded_corpus)
        n_grams = tuple(tuple(word for word in sent if word) for sent in n_grams if sent)
        self.n_grams = tuple(n_grams)
        return 0

    def get_n_grams_frequencies(self) -> int:
        """
        Fills in the n-gram storage from a sentence, fills the field n_gram_frequencies
        :return: 0 if succeeds, 1 if not
        e.g.
        self.n_grams = (
            (
                ((1, 2), (2, 3), (3, 4), (4, 1)), ((1, 5), (5, 2), (2, 1))),
                (((1, 3), (3, 4), (4, 1)), ((1, 5), (5, 2), (2, 1))
            )
        )
        --> {
            (1, 2): 1, (2, 3): 1, (3, 4): 2, (4, 1): 2,
            (1, 5): 2, (5, 2): 2, (2, 1): 2, (1, 3): 1
        }
        """
        if not self.n_grams:
            return 1

        for sentence in self.n_grams:
            for word in sentence:
                for n_gram in word:
                    if n_gram not in self.n_gram_frequencies:
                        self.n_gram_frequencies[n_gram] = 0
                    else:
                        self.n_gram_frequencies[n_gram] += 0

        return 0


#---------------------------------------------------------
    def extract_n_grams_frequencies(self, n_grams_dictionary: dict) -> int:
        if not isinstance(n_grams_dictionary, dict):
            return 1
        for n_gram, freq in n_grams_dictionary.items():
            if isinstance(n_gram, tuple):
                self.n_gram_frequencies[n_gram] = freq
        return 0
        
    
    def extract_n_grams_log_probabilities(self, n_grams_dictionary: dict) -> int:
        pass

    def calculate_log_probabilities(self) -> int:
        """
        Gets log-probabilities of n-grams, fills the field n_gram_log_probabilities
        :return: 0 if succeeds, 1 if not
        """
    
class LanguageProfile:
    '''
    Stores and manages language profile information
    '''
    def __init__(self, letter_storage: LetterStorage, language_name: str):
        self.storage = letter_storage
        self.language = language_name
        self.tries = []
        self.n_words = []

    def create_from_tokens(self, encoded_corpus: tuple, ngram_sizes: tuple) -> int:
        if (not isinstance(encoded_corpus, tuple)
                or not isinstance(ngram_sizes, tuple)):
            return 1
        for size in ngram_sizes:
            trie = NGramTrie(size, self.storage)
            trie.extract_n_grams(encoded_corpus)
            trie.get_n_grams_frequencies()
            self.tries.append(trie)
            self.n_words.append(len(trie.n_gram_frequencies))
        return 0

    def get_top_k_n_grams(self, k: int, trie_level: int) -> tuple:
        if not isinstance(k, int)\
               or not isinstance(trie_level, int)\
               or k <= 0:
            return()
        for n_gram_trie in self.tries:
            if n_gram_trie.size == trie_level:
                frequency = n_gram_trie.n_gram_frequencies
                top_k_n_grams = tuple(sorted(frequency, key=frequency.get, reverse = True)[:k])
                return top_k_n_grams
        return()

    # 8
    def save(self, name: str) -> int:
        if not isinstance(name, str):
            return 1
        profile_as_dict = {}
        freq_dict = {}

        for trie in self.tries:
            for key, value in trie.n_gram_frequencies.items():
                string_for_file = ''
                for element in key:
                    string_for_file += self.storage.get_letter_by_id(element)
                freq_dict[string_for_file] = value

        profile_as_dict['freq'] = freq_dict
        profile_as_dict['n_words'] = self.n_words
        profile_as_dict['name'] = self.language
        with open(name, 'w', encoding="UTF-8") as file:
            json.dump(profile_as_dict, file)
        return 0
