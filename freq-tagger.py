def extract_words(test_file,test_words_file):
    test_words = open(test_words_file, 'w')
    with open(test_file) as f:
        for line in f:
            for word in line.split():
                test_words.write(str((word.partition("/")[0])) + "\n")

def get_emissions_line(test_words_file,emissions_file, test_fbtagger_file):
    test_fbtagger = open(test_fbtagger_file, 'w')
    with open(test_words_file) as f1:

            for line1 in f1:
                test_word = line1.replace("\n", "")
                max_mle = -1.0
                max_tag = ""

                with open(emissions_file) as f2:
                    for line2 in f2:
                        w = line2.partition("/")[0]
                        word = w.partition(",")[2].replace(" ", "")
                        m = line2.partition("/")[2]
                        tag = m.partition(",")[0]
                        if m.split(",")[1] == "":
                            mle = 0.0
                        else:
                            mle = float(m.split(",")[1])
                        if test_word == word:
                            if (mle > max_mle):
                                max_mle = mle
                                max_tag = tag
                    if max_mle == -1.0:
                        sentence = str(test_word) + "/NNP" + "\n"
                        test_fbtagger.write(sentence)
                    else:
                        sentence = str(test_word) + "/" + max_tag + "\n"
                        test_fbtagger.write(sentence)


'''Program Execution'''
test_file = "/Users/linda/PycharmProjects/Homework-2/test.txt"
test_words_file = "/Users/linda/PycharmProjects/Homework-2/test_words.txt"
emissions_file = "/Users/linda/PycharmProjects/Homework-2/emissions.txt"
test_fbtagger_file = "/Users/linda/PycharmProjects/Homework-2/test-fbtagger.txt"

extract_words(test_file, test_words_file)
get_emissions_line(test_words_file, emissions_file, test_fbtagger_file)