from collections import Counter


'''general use methods'''
def get_specific_word_count(file, word):
    f = open(file).read()
    count = f.count(word)
    return count

def get_word_pair_count(word_pairs):
    word_pair_count = Counter(word_pairs)
    for k, v in word_pair_count.items():
        print(k, " ", v)

def number_of_token(file):
    n = 0
    with open(file) as f:
        count = Counter(f.read().split())
        for k, v in count.items():
            n += v
    return n

'''transitions.txt'''
def get_tags(train_file, train_tags_file):
    tags_file = open(train_tags_file, 'w')
    with open(train_file, 'r') as f:
        for line in f:
            for word in line.split():
                tags_file.write("<s> " + str(word.partition("/")[2]) + " </s>" + "\n")

def compute_transition_MLE_helper(train_tags_file, word, frequency): #where the MLE algorithm is
    word_count = get_specific_word_count(train_tags_file, word[0])
    MLE = frequency/word_count
    return MLE


def compute_transition_MLE(train_tags_file, transitions_file):
    transitions = open(transitions_file, 'w')
    word_pairs = []
    with open(train_tags_file) as f:
        data = iter(f.read().split())
        x = (data)
        y = next(data)
    while True:
        try:
            if x is not y:
                x = y
                y = next(data)
                word_pairs.append(tuple((x,y)))
            else:
                x = next(data)
                y = next(data)
                word_pairs.append(tuple((x,y)))
        except StopIteration:
            break
    count = Counter(word_pairs)
    for k,v in count.items():
        MLE = compute_transition_MLE_helper(train_tags_file,k,v)
        line = str(k) + " " + str(v) + " " + str(MLE) + "\n"
        transitions.write(line)

# COMPARE: how many lines do you have in your transitions text
#          McGrawHill? Tag Counts?

'''emissions.txt'''
def write_to_emissions_file(emissions_file, train_tags_file, train_file):
    emissions = open(emissions_file, 'w')
    N = number_of_token(train_file)
    tags = []
    word_and_tags = []

    #TAGS
    with open(train_tags_file) as f:
        for line in f:
            tags.append(line[4:line.index("/") - 2])
    count_tags = Counter(tags)
    print(count_tags)

    #WORD AND TAG
    train = open(train_file)
    for word in train.read().split():
        word_and_tags.append(word)
    count_word_and_tags = Counter(word_and_tags)

    for k,v in count_tags.items():
        for i,j in count_word_and_tags.items():
            if k in i:
                mle = j / v
                laplace = (j + 1) / (j + 1 + N)
                # print(k, " ", i, " ", j, " ", v)

                #prints: TAG, WORD_AND_TAG, MLE, LAPLACE
                line = str(k) + ", " + str(i) + ", " + str(mle) + ", " + str(laplace) + "\n"
                emissions.write(line)

# COMPARE: do we count the line numbers as unique
#           LAPLACE??

'''laplace-tag-unigrams.txt'''
def write_laplace_tag_unigram(laplace_tag_unigram_file, train_tags_file, train_file):
    laplace_tag_unigram = open(laplace_tag_unigram_file, 'w')
    N = number_of_token(train_file)
    tags = []
    #TAGS
    with open(train_tags_file) as f:
        for line in f:
            tags.append(line[4:line.index("/") - 2])
    count_tags = Counter(tags)

    for k,v in count_tags.items():
        mle = (v+1)/(v + 1 + N)
        line = str(k) + ", " + str(mle) + "\n"
        laplace_tag_unigram.write(line)

#COMPARE: check unigram laplace formula

'''Program Execution'''
train_file = "/Users/linda/PycharmProjects/Homework-2/train.txt"
train_tags_file = "/Users/linda/PycharmProjects/Homework-2/train_tags.txt"
transitions_file = "/Users/linda/PycharmProjects/Homework-2/transitions.txt"
emissions_file = "/Users/linda/PycharmProjects/Homework-2/emissions.txt"
laplace_tag_unigram_file = "/Users/linda/PycharmProjects/Homework-2/laplace-tag-unigrams.txt"

get_tags(train_file, train_tags_file)
#PART1.1
compute_transition_MLE(train_tags_file, transitions_file)
#PART1.2
write_to_emissions_file(emissions_file,train_tags_file, train_file)
#PART1.3
write_laplace_tag_unigram(laplace_tag_unigram_file, train_tags_file, train_file)
