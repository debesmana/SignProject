text = raw_input("Input here")
words = text.split()
words_list = {}
word_count = 0
for i in words:
    if i not in words_list:
        words_list[i] = word_count
    else:
        word_count = word_count + 1
        words_list[i] = word_count
print words_list
