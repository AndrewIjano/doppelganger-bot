import nltk
import pprint
import random

nltk.download('punkt')

with open('speeches.txt', encoding='utf-8') as speeches_file:
    speeches = speeches_file.read()

sentences = nltk.sent_tokenize(speeches)

table = {}

for sentence in sentences:
    words = sentence.split()
    keys = words[:2]
    table.setdefault('#BEGIN', []).append(keys[:])

    for word in words[2:]:
        table.setdefault(tuple(keys), []).append(word)
        keys.pop(0)
        keys += [word]

    table.setdefault('#END', []).append(keys[:][1:])

# print(random.choice(table['#BEGIN']))

for i in range(10):
    n = 100
    key = random.choice(table['#BEGIN'])
    # print(key)
    msg = ' '.join(key)

    for _ in range(n):
        new_key = table.setdefault(tuple(key))
        # print(new_key)
        if (new_key == '' or new_key is None):
            break


        new_word = random.choice(new_key)
        msg += ' ' + new_word

        key.pop(0)
        key.append(new_word)

        if (new_word in table['#END']):
            break

    print(msg)
    

pprint.pprint(table)