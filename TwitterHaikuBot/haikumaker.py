# badhaikubot.py
# A twitter bot that turns a tweet into a really bad haiku
# Made by: https://github.com/Triple3Apple

import syllapy
import random


# word = 'because'
# print('syllable count for ' + word + ' is: ' + str(syllapy.count(word)))

special_words = ['the', 'an', 'or', 'and', 'is',
                 'i', 'that', 'he', 'she', 'they',
                 'are', 'for', 'in', 'my', 'all',
                 'our', 'to', 'as', 'of']


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
    
    line1 = form_haiku_line(syllable_words.copy(), indexes_with_words, 5)
    line2 = form_haiku_line(syllable_words.copy(), indexes_with_words, 7)
    line3 = form_haiku_line(syllable_words.copy(), indexes_with_words, 5)
    
    haiku = line1 + '\n' + line2 + '\n' + line3
    
    print('\n\n--------\n' + haiku + '\n\n--------\n')
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
    chars_to_remove = [';', ':', '!', '*', '#', ',', '?', '"', '&']
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

    #print(str(special_words))

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

    # add distibution values for each syllable
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
    last_word_chosen = ''
    
    while current_syllable_count < num_of_syllables:
    #    syllable_choice = random.randint(0, len(syllable_indexes))
    
        # choose a syllable based on weights
        print('syllable indexes: ' + str(syllable_indexes))
        # syllable_choices = random.choices(syllable_indexes, cum_weights=distribution_array, k=1)
        syllable_choices = random.choices(syllable_indexes, weights=distribution_array, k=1)
        print('result after random.choices: ' + str(syllable_choices))
        syllable_choice_num = syllable_choices[0]
        # to make it represent syllable num not index
        syllable_choice_num += 1
        
        # checking if current syllable choice will exceed amount needed
        if current_syllable_count + syllable_choice_num > num_of_syllables:
            # TODO: might need more checking (there could be a infinite loop)
            error_loop_count += 1
            
            if error_loop_count > 50:
                # break out of loop, no compatible syllable value was found (NOT GOOD)
                print("ERROR: could not choose a correct syllable value in form_haiku_line()")
                break
            
            # continue to try to find a good syllable value
            # TODO: find a better non-random way to get a correct syllable count!!!!!!
            continue

        error_loop_count = 0

        print('******syllable num chosen: ' + str(syllable_choice_num) + '******')

        # choose a random word from the list inside syllable_words list
        words = syllable_words[syllable_choice_num - 1]
        print('syllable_words' + str(syllable_words[syllable_choice_num - 1]))
        print(str(words))
        curr_word = random.choice(words)
        # curr_word = random.choice(syllable_words[syllable_choice_num - 1])
        print('word chosen: ' + curr_word)
        
        non_rand_index = 0
        is_error = False
        
        print('checking word...')
        
        # meaning that there is only one word that has that many syllables
        while last_word_chosen.lower() == curr_word.lower():
            
            # if there is only one word that has this many syllables,
            # then retry and pick a diff syllable num
            if len(syllable_words[syllable_choice_num - 1]) == 1:
                print('There is only 1 word that matches this syllable count: ' + str(syllable_words[syllable_choice_num - 1]))
                print('retrying...')
                is_error = True
                break   # break out of *this* while loop

            # if non_rand_index is greater than the allowed indexes, break
            if non_rand_index >= len(syllable_words[syllable_choice_num - 1]):
                print('ERROR, could not find a dif word (bug most likely!) in form_haiku_line()')
                is_error = True
                break
            
            print('word is same as the last one, choosing a dif word with ' + str(syllable_choice_num) + ' syllable')
            
            # choose a different word
            word_arr = syllable_words[syllable_choice_num - 1]
            curr_word = word_arr[non_rand_index]
            print('new word chosen: ' + curr_word)
            print('checking word...')
            non_rand_index += 1

        if is_error is True:
            continue
        
        loopNum = 0
        
        # check if this is the last word and if it is a special word
        curr_word_temp = curr_word
        if (curr_word_temp.lower() in special_words) and ((syllable_choice_num + current_syllable_count) == num_of_syllables):
            print('word is special word: ' + curr_word_temp + '  retrying...')
            loopNum += 1
            if loopNum > 50:
                print('ERROR, couldnt find word that was not special num-------------------------------')
                break
            continue

        print('new word is correct :)  : ' + curr_word)
        
        # make first letter of the word capital
        if current_syllable_count == 0:
            curr_word = curr_word.capitalize()
        else:
            curr_word = curr_word.lower()
            

        # update current_syllable_count
        current_syllable_count += syllable_choice_num
        print('curr syllable count is updated: ' + str(current_syllable_count))
        
        # updating last_word_chosen
        last_word_chosen = curr_word

        # adding word to the haiku_line
        if current_syllable_count == num_of_syllables:
            # end of the haiku line
            haiku_line += curr_word
        else:
            haiku_line += (curr_word + space)
        
        print('haiku line:: ' + haiku_line)

    debug_final_line = f"Final Haiku Line({str(num_of_syllables)} syllables): {haiku_line}"
    print('-----------------------------------')
    print(debug_final_line)
    print('-----------------------------------')
    
    return haiku_line
