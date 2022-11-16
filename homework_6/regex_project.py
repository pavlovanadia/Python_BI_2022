import re
import matplotlib.pyplot as plt


# task 1

#pattern_1 = r'(ftp\S[\w\./#]*\.\w*)[\s;]' # this regex was when i got the update that only links with .format in the end count
pattern_1 = r'(ftp\S[\w\./#]*)' # this regex parses all ftp links regardless of format presence
res = set()
with open('references.txt') as inp, open ('ftps', 'w') as out, open ('unique_ftps', 'w') as out_2:
    for line in inp:
        for i in re.findall(pattern_1, line):
            out.write(i + '\n')
            if i not in res:
                out_2.write(i + '\n')
            res.add(i)


# task 2

pattern_2 = r'\d+[.,]?\d+'
with open('2430AD.txt') as inp:
    for line in inp:
        for i in re.findall(pattern_2, line):
            print(i)


# task 3

pattern_3 = r'[a-zA-z]*[Aa][a-zA-z]*'
with open('2430AD.txt') as inp:
    for line in inp:
        for i in re.findall(pattern_3, line):
            print(i)


# task 4

pattern_4 = r'[A-Z][^!?\.]*!'
with open('2430AD.txt') as inp:
    for line in inp:
        for i in re.findall(pattern_4, line):
            print(i)


# task 5
# here we need to know that the longest word in English has the length of 45 characters 
# https://en.wikipedia.org/wiki/Longest_word_in_English 
# i understand that in that text we have shorter words, bur this kind of code would be applecable to any text
# here numbers also counted as words

word_lengths = dict()
for length in range(1, 46):
    word_lengths[length] = set()
    ptr = r'\b\w{' + str(length) + r'}\b' # i really wanted to combine string formatting and raw strings but totally failed
    with open('2430AD.txt') as inp:
        for line in inp:
            for word in re.findall(ptr, line):
                word_lengths[length].add(word.lower())

word_lengths = dict((k, len(v)) for k, v in word_lengths.items())
word_lengths


# task 5.2
# here we need to know that the longest word in English has the length of 45 characters 
# https://en.wikipedia.org/wiki/Longest_word_in_English 
# i understand that in that text we have shorter words, bur this kind of code would be applecable to any text
# ONLY words from letters, no numbers

word_lengths_2 = dict()
for length in range(1, 46):
    word_lengths_2[length] = set()
    ptr = r'\b[A-Za-z]{' + str(length) + r'}\b' # i really wanted to combine string formatting and raw strings but totally failed
    with open('2430AD.txt') as inp:
        for line in inp:
            for word in re.findall(ptr, line):
                word_lengths_2[length].add(word.lower())

word_lengths_2
word_lengths_2 = dict((k, len(v)) for k, v in word_lengths_2.items())
word_lengths_2


# barplot, numbers are assumed to be words
# as far as i can use only one external library and it is not pandas ;-( i choose plt bar bcs it is easy to make a plot from dict

plt.bar(list(word_lengths.keys()), word_lengths.values(), color='b')
plt.title("Unique words (with numbers) lengths count")
plt.xlabel("Word length")
plt.ylabel("Word count")
plt.show()


# barplot, numbers are not counted as words
# as far as i can use only one external library and it is not pandas ;-( i choose plt bar bcs it is easy to make a plot from dict

plt.bar(list(word_lengths_2.keys()), word_lengths_2.values(), color='y')
plt.title("Unique words (without numbers) lengths count")
plt.xlabel("Word length")
plt.ylabel("Word count")
plt.show()


# okay we see here that in this story the full potential of English word length is not used by author
# so i can change x axis a bit so that plots would look nicer and put them on the same plot
# and not in absolute count but in proportion
# i can see that the maximum word length in the novel is 15, so i can exclude all keys bigger than that
# omg i miss pandas sooo much
# so first would be process the data

zero_count_lenght = list(i for i in range(16, 46)) # list of word lengths with 0 count

""" return another dict without keys from a list """
def without_keys(d, keys):
    return {k: d[k] for k in d.keys() - keys}

""" return a dict with proportions """
def proportion(d):
    all_sum = sum(d.values())
    return {k: d[k] / all_sum for k in d.keys()}

w_l_num_short = proportion(without_keys(word_lengths, zero_count_lenght)) # number are words
w_l_short = proportion(without_keys(word_lengths_2, zero_count_lenght)) # numbers are not words


fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 15))

ax1.bar(list(w_l_num_short.keys()), w_l_num_short.values(), color='b')
ax2.bar(list(w_l_short.keys()), w_l_short.values(), color='y')
ax3.bar(list(w_l_num_short.keys()), w_l_num_short.values(), color='b', alpha=0.7)
ax3.bar(list(w_l_short.keys()), w_l_short.values(), color='y', alpha=0.7)

ax1.set_title("Unique words (with numbers) lengths count")
ax2.set_title("Unique words (without numbers) lengths count")
ax3.set_title("Unique words (with and without numbers) lengths count")
ax1.set_xticks(list(i for i in range(1, 16)), fontsize=1)
ax1.xaxis.set_tick_params(labelsize=7)
ax2.set_xticks(list(i for i in range(1, 16)), fontsize=1)
ax2.xaxis.set_tick_params(labelsize=7)
ax3.set_xticks(list(i for i in range(1, 16)), fontsize=1)
ax3.xaxis.set_tick_params(labelsize=7)
ax1.set_xlabel("Word length")
ax2.set_xlabel("Word length")
ax3.set_xlabel("Word length")
ax1.set_ylabel("Word count proportion")
ax2.set_ylabel("Word count proportion")
ax3.set_ylabel("Word count proportion")
;


# task 6

pattern_6 = r'([БбВвГгДдЖжЗзЙйКкЛлМмНнПпРрСсТтФфХхЦцЧчШшЩщ]*)([АаЕеЁёИиОоУуЫыЭэЮюЯя])'
def brikick(text):
    res = []
    for word in text.split():
        res.append(re.sub(pattern_6, r'\1' + r'\2' + 'к' + r'\2', word))
    return ' '.join(res)


# task 7

pattern_7 = r'([A-ZА-Я][^!?\.]*[!?\.])' # sentences have to be closed with . ! or ? works with both latin and cyrillic characters

# no number is assumed as a word
# i wated to create a beautiful regex but i created a monster
pattern_8 = r'[\'\"]?([A-Za-zА-Яа-я]*[-\']?[A-Za-zА-Яа-я]*[-\']?[A-Za-zА-Яа-я]*[-\']?[A-Za-zА-Яа-я]+)[\'\"]?[-:,]?[\s\.!?]' 


def find_n_words_sentences(text, n):
    ans = []
    for i in re.findall(pattern_7, text):
        if len(re.findall(pattern_8, i)) == n:
            ans.append(tuple(i for i in re.findall(pattern_8, i)))
    return ans

# here i provide a couple of commented test strings for different lengths and weird punctuation usage
# test_len = "Здесь три слова. Тут два? Здесь их уже четыре. Одно? Как думаешь, может, их пять?"
# weird_punct_test = "Д'Артаньян это кто? 'Д'Арк-Кусто' странная фамилия. Кусто-Д'Арк- не лучше. Слово 'он-лайн-конференция' - устарело."
# n = 3

# find_n_words_sentences(weird_punct_test, n)
