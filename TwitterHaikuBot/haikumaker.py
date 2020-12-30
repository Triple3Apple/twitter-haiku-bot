import syllapy


word = 'because'
print('syllable count for ' + word + ' is: ' + str(syllapy.count(word)))


def make_haiku(text: str):
    if not text:
        print('Error: text of tweet is empty :(')
        return
    print('RECIEVED TEXT: ' + text)


def seperate_to_syllables():
    return True
