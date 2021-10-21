"""
Lab 2
Language classification
"""

from lab_1.main import tokenize, remove_stop_words

# 2
import json


def tokenize(text: str) -> list or None:
    """
    Splits a text into tokens, converts the tokens into lowercase,
    removes punctuation and other symbols from words
    :param text: a text
    :return: a list of lower-cased tokens without punctuation
    """
    if not isinstance(text, str):
        return None
    text = text.lower()
    preprocessed = ''
    for symbol in text:
        if symbol.isalnum() or symbol == ' ':
            preprocessed += symbol
    tokens = preprocessed.split()
    return tokens


def remove_stop_words(tokens: list, stop_words: list) -> list or None:
    """
    Removes stop words
    :param tokens: a list of tokens
    :param stop_words: a list of stop words
    :return: a list of tokens without stop words
    """
    if not isinstance(tokens, list) or not isinstance(stop_words, list):
        return None
    tokens = [token for token in tokens if token not in stop_words]
    return tokens


def get_freq_dict(tokens: list) -> dict or None:
    """
    Calculates frequencies of given tokens
    :param tokens: a list of tokens
    :return: a dictionary with frequencies
    """
    if not isinstance(tokens, list):
        return None
    for word in tokens:
        if not isinstance(word, str):
            return None
    freq_dict = {}
    for token in tokens:
        if token in freq_dict:
            freq_dict[token] += 1/len(tokens)
        else:
            freq_dict[token] = 1/len(tokens)
    return freq_dict


def get_language_profiles(texts_corpus: list, language_labels: list) -> dict or None:
    if not isinstance(texts_corpus, list) or not isinstance(language_labels, list):
        return None
    profiles = dict()
    for i in range(len(language_labels)):
        profiles[language_labels[i]] = get_freq_dict(texts_corpus[i])
    return profiles


def get_language_features(language_profiles: dict) -> list or None:
    if not isinstance(language_profiles, dict):
        return None
    features = list()
    for profile in language_profiles:
        features += language_profiles[profile].keys()
    return sorted(features)


def get_text_vector(original_text: list, language_profiles: dict) -> list or None:
    if not isinstance(language_profiles, dict) or not isinstance(original_text, list):
        return None

    text_vector = list()
    for text in original_text:
        text_in_profile = list()
        for profile in language_profiles:
            if text in language_profiles[profile]:
                text_in_profile.append(language_profiles[profile][text])
            else:
                text_in_profile.append(0)
        text_vector.append(max(text_in_profile))
    return text_vector


def get_text_vector1(original_text: list, language_profiles: dict) -> list or None:
    if not isinstance(language_profiles, dict) or not isinstance(original_text, list):
        return None

    text_vector = list()
    for text in get_language_features(language_profiles):
        if text in original_text:
            for profile in language_profiles:
                if text in language_profiles[profile]:
                    text_vector.append(language_profiles[profile][text])
        else:
            text_vector.append(0)
    return text_vector


def calculate_distance(unknown_text_vector: list, known_text_vector: list) -> float or None:
    if not isinstance(known_text_vector, list) or not isinstance(unknown_text_vector, list):
        return None
    s = 0
    for i in range(len(unknown_text_vector)):
        s += (unknown_text_vector[i] - known_text_vector[i]) ** 2
    return s ** 0.5


def predict_language_score(unknown_text_vector: list, known_text_vectors: list, language_labels: list) -> [str, int]\
                                                                                                          or None:
    if not isinstance(known_text_vectors, list) or not isinstance(unknown_text_vector, list) or\
            not isinstance(language_labels, list):
        return None
    best_result = 0
    label = ""
    for i in range(len(known_text_vectors)):
        calc = calculate_distance(unknown_text_vector, known_text_vectors[i])
        if i == 0:
            best_result = calc
            label = language_labels[i]
        if calc <= best_result:
            best_result = calc
            label = language_labels[i]
    return [label, best_result]


def calculate_distance_manhattan(unknown_text_vector: list, known_text_vector: list) -> float or None:
    if not isinstance(known_text_vector, list) or not isinstance(unknown_text_vector, list):
        return None
    s = 0
    for i in range(len(unknown_text_vector)):
        s += abs(unknown_text_vector[i] - known_text_vector[i])
    return s


def predict_language_knn(unknown_text_vector: list, known_text_vectors: list, language_labels: list, k=1, metric='manhattan') -> [str, int] or None:
    if not isinstance(known_text_vectors, list) or not isinstance(unknown_text_vector, list) or \
            not isinstance(language_labels, list):
        return None
    res = list()
    for i in range(len(known_text_vectors)):
        if metric == 'manhattan':
            calc = calculate_distance_manhattan(unknown_text_vector, known_text_vectors[i])
        else:
            calc = calculate_distance(unknown_text_vector, known_text_vectors[i])
        res.append([calc, language_labels[i]])
    print(res)
    res = sorted(res, key=lambda x: x[0])[:k]
    print(res)

    scores = dict()
    for i in res:
        if i[1] in scores:
            scores[i[1]] += 1
        else:
            scores[i[1]] = 1
    print(scores)
    for i in scores:
        if scores[i] == max(scores.values()):
            lbl = i
            break
    for i in res:
        if i[1] == lbl:
            return [lbl, i[0]]


# 10 implementation
def get_sparse_vector(original_text: list, language_profiles: dict) -> list or None:
    """
    Builds a sparse vector representation of a given text
        using dictionary with language profiles
    :param original_text: any tokenized text
    :param language_profiles: a dictionary of dictionaries - language profiles
    """
    pass


def calculate_distance_sparse(unknown_text_vector: list,
                              known_text_vector: list) -> float or None:
    """
    Calculates distance between two vectors using euclid metric
    :param unknown_text_vector: sparse vector for unknown text
    :param known_text_vector: sparse vector for known text
    """
    pass


def predict_language_knn_sparse(unknown_text_vector: list, known_text_vectors: list,
                                language_labels: list, k=1) -> [str, int] or None:
    """
    Predicts unknown text label and its distance to the closest known text
        using knn based algorithm
    :param unknown_text_vector: sparse vector for unknown text
    :param known_text_vectors: a list of sparse vectors for known texts
    :param language_labels: language labels for each known text
    :param k: the number of neighbors to choose label from
    """
    pass
