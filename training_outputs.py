from collections import defaultdict
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



'''Program Execution'''
train_file = "/Users/linda/PycharmProjects/Homework-2/train.txt"
train_tags_file = "/Users/linda/PycharmProjects/Homework-2/train_tags.txt"
transitions_file = "/Users/linda/PycharmProjects/Homework-2/transitions.txt"
get_tags(train_file, train_tags_file)
compute_transition_MLE(train_tags_file, transitions_file)