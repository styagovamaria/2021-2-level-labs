"""
Language detection starter
"""

import os

PATH_TO_LAB_FOLDER = os.path.dirname(os.path.abspath(__file__))
PATH_TO_PROFILES_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'profiles')
PATH_TO_DATASET_FOLDER = os.path.join(PATH_TO_LAB_FOLDER, 'dataset')

if __name__ == '__main__':
    with open(os.path.join(PATH_TO_PROFILES_FOLDER, 'eng.txt'),
              'r', encoding='utf-8') as file_to_read:
        EN_TEXT = file_to_read.read()

    with open(os.path.join(PATH_TO_PROFILES_FOLDER, 'de.txt'),
              'r', encoding='utf-8') as file_to_read:
        DE_TEXT = file_to_read.read()

    with open(os.path.join(PATH_TO_PROFILES_FOLDER, 'lat.txt'),
              'r', encoding='utf-8') as file_to_read:
        LAT_TEXT = file_to_read.read()

    with open(os.path.join(PATH_TO_DATASET_FOLDER, 'known_samples_de.txt'),
              'r', encoding='utf-8') as file_to_read:
        DE_SAMPLES = file_to_read.read().split('[TEXT]')[1:]

    with open(os.path.join(PATH_TO_DATASET_FOLDER, 'known_samples_eng.txt'),
              'r', encoding='utf-8') as file_to_read:
        EN_SAMPLES = file_to_read.read().split('[TEXT]')[1:]

    with open(os.path.join(PATH_TO_DATASET_FOLDER, 'known_samples_lat.txt'),
              'r', encoding='utf-8') as file_to_read:
        LAT_SAMPLES = file_to_read.read().split('[TEXT]')[1:]

    with open(os.path.join(PATH_TO_DATASET_FOLDER, 'unknown_samples.txt'),
              'r', encoding='utf-8') as file_to_read:
        UNKNOWN_SAMPLES = file_to_read.read().split('[TEXT]')[1:]
        #print(main.get_freq_dict(main.tokenize(de_text)))

    # corpus = [main.tokenize(en_text), main.tokenize(de_text), main.tokenize(la_text)]
    # labels = ['eng', 'de', 'la']

    corpus = [
        ['the', 'boy', 'is', 'playing', 'football'],
        ['der', 'junge', 'der', 'fussball', 'spielt']
    ]
    labels = ['eng', 'de']

    profiles = main.get_language_profiles(corpus, labels)
    print(profiles)
    print(main.get_language_features(profiles))
    # 4
    original_text = ['this', 'boy', 'is', 'playing', 'football']
    print(main.get_text_vector1(original_text, profiles))

    # 5
    unknown_text_vector = [0.2, 0, 0.2, 0, 0.2, 0, 0.2, 0, 0]
    known_text_vector = [0, 0.2, 0, 0.1, 0, 0.49, 0, 0.3, 0]
    print(main.calculate_distance(unknown_text_vector, known_text_vector))

    # 6
    unknown_text_vector = [0.2, 0, 0.2, 0, 0.2, 0, 0.2, 0, 0]
    known_text_vectors = [
        [0, 0.2, 0, 0.1, 0, 0.49, 0, 0.3, 0],
        [0.1, 0, 0.4, 0.1, 0, 0, 0.34, 0.3, 0],
        [0, 0.2, 0, 0.1, 0, 0.49, 0, 0.3, 0.35]
    ]
    language_labels = ['eng', 'de', 'eng']

    print(main.predict_language_score(unknown_text_vector, known_text_vectors, language_labels))

    # 7
    print(main.calculate_distance_manhattan(unknown_text_vector, known_text_vectors[0]))

    # 8
    unknown_text_vector = [0.2, 0, 0.2, 0, 0.2, 0, 0.2, 0, 0]
    known_text_vectors = [
        [0, 0.2, 0, 0.1, 0, 0.49, 0, 0.3, 0],
        [0.1, 0, 0.4, 0.1, 0, 0, 0.34, 0.3, 0],
        [0, 0.2, 0, 0.1, 0, 0.49, 0, 0.3, 0.35],
        [0.11, 0, 0.34, 0.1, 0.12, 0, 0.8, 0.1234, 0.1],
        [0.1, 0, 0.4, 0.1, 0.1, 0.11, 0.34, 0.3, 0],
        [0, 0, 0.4, 0, 0, 0, 0.6, 0.3, 0.3456]
    ]
    language_labels = ['eng', 'de', 'eng', 'eng', 'de', 'de']
    k = 3
    metric = 'euclid'

    print(main.predict_language_knn(unknown_text_vector, known_text_vectors, language_labels, k, metric))
    
    EXPECTED = ['de', 'eng', 'lat']
    RESULT = ''
    # DO NOT REMOVE NEXT LINE - KEEP IT INTENTIONALLY LAST
    assert RESULT, 'Detection not working'
