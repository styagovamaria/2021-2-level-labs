from lab_4.main import tokenize_by_letters
from lab_4.main import  LetterStorage
from lab_4.language_profile import LanguageProfile
from lab_4.main import tokenize_by_letters, NGramTextGenerator
from lab_4.main import LetterStorage, encode_corpus, LikelihoodBasedTextGenerator

text = 'bla blabla'

print(tokenize_by_letters(text))

with open('reference_text.txt', 'r', encoding='utf-8') as f:
    text_from_file = f.read()
    f.close()

#text_from_file = 'Steve man! Take me by the hand, bring me to the land that you understand'
text_tok = tokenize_by_letters(text_from_file)
s = LetterStorage()
s.update(text_tok)
storage_list = list(s.storage)
print(storage_list)
print('5 lowest id literals:{}'.format( storage_list[:5]))
print('5 higest id literals:{}'.format( storage_list[-5:]))



# for 6
encoded = encode_corpus(s, text_tok)

profile = LanguageProfile(s, 'en')
#profile.create_from_tokens(encoded, (2,))
profile.create_from_tokens(encoded, (2,))

text_generator = NGramTextGenerator(profile)
sentences = []
words=[]
for word_lenght in range(2,8):
    words.append(text_generator._generate_word((2,),word_lenght))


for sentence_length in range(5, 20):
    sentences.append(text_generator.generate_decoded_sentence((1,), sentence_length))

for sentence in sentences:
    print(sentence)

generator = LikelihoodBasedTextGenerator(profile)
for length in range(5, 11):
    print(generator.generate_decoded_sentence((1,), length))