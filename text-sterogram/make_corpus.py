import pickle

words = open('words.txt')
word_list = []

lines = words.readlines()
for l in lines:
    word = l.strip()
    if 3 <= len(word) <= 6:
        word_list.append(word)

pickle.dump(word_list, open('words.pickle', 'wb'))
