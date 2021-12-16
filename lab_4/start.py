from lab_4.main import tokenize_by_letters
from lab_4.main import  LetterStorage

text = 'bla blabla'

print(tokenize_by_letters(text))

with open('reference_text.txt', 'r', encoding='utf-8') as f:
    text_from_file = f.read()

text_tok = tokenize_by_letters(text_from_file)
s = LetterStorage()
s.update(text_tok)

letters_count = s.get_letter_count()
storage_list = []
for key in s.storage:
    print(s.storage[key])
    print(key)
    storage_list.append(key)

print('Count of literals: {}'.format(letters_count))
print('5 lowest id literals:{}'.format( storage_list[:5]))
print('5 higest id literals:{}'.format( storage_list[-5:]))

