import syllapy


word = 'because'
print('syllable count for ' + word + ' is: ' + str(syllapy.count(word)))


def make_haiku(text: str):

    haiku = ''

    # testing
    test = ["hey", "2020", "why2"]
    filter_out_words(test)
    print(str(test))

    words_list = seperate_to_syllables(text)

    print('before filtering: ')
    print(words_list[0:])

    filter_out_words(words_list)

    print('filtered word list:')
    print(words_list[0:])

    if not text:
        print('Error: text of tweet is empty :(')
        return
    print('RECIEVED TEXT: ' + text)

    return haiku


def seperate_to_syllables(text_with_spaces: str):

    words_list = text_with_spaces.split()

    print('seperating str to words')
    print(words_list[0:])

    return words_list


def filter_out_words(unfiltered_words: list):

    words_to_remove = []
    words_to_edit = []
    chars_to_remove = [';', ':', '!', '*', '#', ',', '?']

    for word in unfiltered_words:
        # if any(char.isdigit() for char in word):
        print('analyzing: ' + word)
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
        
        
            
