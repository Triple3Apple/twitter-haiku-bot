import syllapy
import random


word = 'because'
print('syllable count for ' + word + ' is: ' + str(syllapy.count(word)))


def make_haiku(text: str):

    haiku = ''
    
    if not text:
        print('Error: text of tweet is empty :(')
        return
    print('RECIEVED TEXT: ' + text)

    # testing
    # test = ["hey", "2020", "why2"]
    # filter_out_words(test)
    # print(str(test))

    words_list = seperate_to_words(text)

    print('before filtering: ')
    print(words_list[0:])

    filter_out_words(words_list)

    print('filtered word list:')
    print(words_list[0:])

    syllable_words = get_syllable_words(words_list.copy())
    
    # get indexes that have syllables
    indexes_with_words = []
    
    for index in range(len(syllable_words)):
        if len(syllable_words[index]) > 0:
            indexes_with_words.append(index)
    
    print('indexes_with_words:' + str(indexes_with_words))
    
    form_haiku_line(syllable_words.copy(), indexes_with_words, 5)
    
    # for syllable_array in syllable_words:
    #     if len(syllable_array) > 0:
    #         indexes_with_words
    
    # turn words into haiku
    

    return haiku


def seperate_to_words(text_with_spaces: str):

    words_list = text_with_spaces.split()

    print('seperating str to words')
    print(words_list[0:])

    return words_list


def filter_out_words(unfiltered_words: list):

    words_to_remove = []
    words_to_edit = []
    chars_to_remove = [';', ':', '!', '*', '#', ',', '?']
    other_bad_chars = ['/']

    for word in unfiltered_words:
        # if any(char.isdigit() for char in word):
        print('analyzing: ' + word)

        # removing words that contain / symbol
        if any(char in other_bad_chars for char in word):
            print('found / symbol in: ' + word)
            unfiltered_words.remove(word)
            continue

        # removing any words that contain numbers
        if any(map(str.isdigit, word)):
            print('found number in: ' + word)
            words_to_remove.append(word)
            continue

        if any(not char.isalnum() for char in word):
            print('found symbol in: ' + word)
            words_to_edit.append(word)
            continue

    for word_to_remove in words_to_remove:
        unfiltered_words.remove(word_to_remove)

    for word_to_edit in words_to_edit:

        if any((char in chars_to_remove) for char in word_to_edit):
            word_index = unfiltered_words.index(word_to_edit)
            unfiltered_words[word_index] = ''.join(i for i in word_to_edit if not i in chars_to_remove)
        else:
            unfiltered_words.remove(word_to_edit)

    # remove duplicate words maybe??


# will organize words in to corresponding arrays
# e.g. syllable_list[0] = will contain an array
# that contains words with 1 syllable

def get_syllable_words(list_of_words: list):

    syllable_list = [[], [], [], [], [], [], [], [], [], []]

    for word in list_of_words:
        syllable_num = syllapy.count(word)
        # ignore words with <10 syllables
        if syllable_num > 10:
            print('WARNING: recieved a syllable count greater than 10, ' + str(syllable_num))
            continue
        if syllable_num < 1:
            print('ERROR: recieved a syllable count less than 1, ' + str(syllable_num))
            continue
        print('analyzed word: ' + word + ', syllables: ' + str(syllable_num))
        # store word in corresponing index which contains an array
        syllable_list[syllable_num - 1].append(word)

    print(str(syllable_list))

    return syllable_list

# forms a haiku line given words organized by syllables,
# indexes that tell which arrays have words in it,
# num_of_syllables which states how many sylllables this
# line requires
# TODO: improve this explanation!!


def form_haiku_line(syllable_words: list, syllable_indexes: list, num_of_syllables: int):

    haiku_line = ''
    space = ' '

    # initializing array with specified size based on the number
    # of syllables present
    
    distribution_array = [0] * len(syllable_indexes)
    
    distribution_array_index = 0
    
    # get total number of words
    total_words_num = 0
    for array in syllable_words:
        for word in array:
            total_words_num += 1

    print('total number of words: ' + str(total_words_num))

    # add distibution values for each 
    for index in range(len(syllable_words)):

        word_count = 0

        # going through each word in the array (if there are any)
        for word in syllable_words[index]:
            word_count += 1

        if word_count != 0:
            # to determine the chance that these types of words will be called
            distr_value = (word_count / total_words_num) * 100  # round this number???
            distribution_array[distribution_array_index] = round(distr_value, 2)
            # increment array_index
            distribution_array_index += 1

    print('distribution array: ' + str(distribution_array))

    # number of syllables in the line
    current_syllable_count = 0
    error_loop_count = 0
    
    while current_syllable_count < num_of_syllables:
    #    syllable_choice = random.randint(0, len(syllable_indexes))
        syllable_choice_num = random.choices(syllable_indexes, cum_weights=distribution_array, k=1)
        
        # checking if current syllable choice will exceed amount needed
        if current_syllable_count + syllable_choice_num > num_of_syllables:
            # TODO: might need more checking (there could be a infinite loop)
            error_loop_count += 1
            
            if error_loop_count > 50:
                # break out of loop
                print("ERROR: could not choose a correct syllable value in form_haiku_line()")
                break
            
            continue
        
        error_loop_count = 0
        
        # TODO: choose a word and then append it to the haiku_line...
    

    return haiku_line
