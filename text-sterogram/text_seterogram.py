import pickle
import random

CORPUS = 'words.pickle' # Pickle file of random words to choose from.

MESSAGE_START = 6   # Line that the secret message starts on.
BLOCK_LEN = 16      # Length of each repeating block. 16 works pretty well.
TEXT_WIDTH = 80     # Length of entire paragraph.

def main():
    # Get secret user message
    message = input("What's your secret message? ")
    message_words = message.split(' ')

    # Load random word corpus
    words = pickle.load(open(CORPUS, 'rb'))

    text = build_autostereogram(words, message_words)
    print(text)

def build_autostereogram(words, message_words):
    """
    Builds a text autostereogram line by line.

    Input : words - list of words to randomly build paragraph from
            message_words - secret message from the user that will be inserted
                            into the autostereogram.
    Output: text - a text autostereogram.
    """

    # Begin output text with some calibration dots that look like this:
    #                   *                *
    text = (TEXT_WIDTH // 2 - BLOCK_LEN // 2) * ' ' + \
           '*' + BLOCK_LEN * ' ' + '*' + '\n'

    message_idx = 0         # Current index into secret message
    message_line = False    # True if operating on line with a word from msg.

    for row in range(len(message_words) + 8):
        if row == MESSAGE_START: message_line = True

        line = ''
        if message_line:
            pattern = generate_pattern(BLOCK_LEN, words,
                        start=(message_words[message_idx]))
            message_idx += 1
            if message_idx == len(message_words): message_line = False

            # A line that contains a word from the hidden message has a unique
            # format. After generating a random pattern that starts with a
            # hidden word, The line will begin with a random word (not the
            # hidden word) from the pattern, followed by the complete pattern.
            pattern_words = pattern.split()
            line += random.choice(pattern_words[1:]) + ' ' + pattern

            # Next, we made a subtle edit to the end of the pattern by removing
            # a character at the end, and then add this. This part creates a
            # spacing of BLOCK_SIZE - 1 between two instances of the hidden
            # word, which will make allow it to be perceived at a different
            # 'depth' from the rest of the text.
            pattern_edit = pattern[:-1]
            line += ' ' + pattern_edit + ' ' 

            # Finally, the pattern is rebuilt with the hidden word and a
            # modified random word from the pattern. This is done such that the
            # rest of the line appears random and is made distinct from the
            # critical part of the text that creates the illusion.
            # TODO: Make pattern generation more natural by only using words
            # that can be easily modified with an extra character. Ex: 'lamb'
            # can become 'lambs', 'tart' can become 'start'.
            pattern_words = pattern_edit.split()
            pattern = pattern_words[0] + ' ' + \
                          random.choice(['s', 't', 'a']) + \
                          ' '.join(w for w in pattern_words[1:])

        else:
            # A non-hidden message line just repeats the pattern until
            # TEXT_WIDTH is reached.
            pattern = generate_pattern(BLOCK_LEN, words)
            line += random.choice(pattern.split()) + ' '
                
        while len(line) < TEXT_WIDTH:
            line += pattern + ' '

        line = line[:TEXT_WIDTH]    # Only keep TEXT_WIDTH characters
        text += line + '\n'

    return text

def generate_pattern(length, corpus, start=''):
    """
    Generates a random pattern of words that is exactly length characters long 
    from words in corpus. (No space as final character.

    Input  : length  - Length of pattern to generate
             corpus - List of words to draw randomly from
             start  - String that must start the pattern. Used for the lines
                      containing secret text.
    Output:  A randomly generated pattern of length characters
    """
    pattern = ''
    if start != '': pattern += start + ' '

    remaining = length - len(pattern)
    while remaining > 0:
        # Choose a random word to add to the pattern. If the addition of this 
        # word leaves too little room, try another. 
        rand_word = random.choice(corpus) 
        while (remaining - len(rand_word) in [1, 2, 3] or 
               len(rand_word) > remaining):
            rand_word = random.choice(corpus) 

        pattern += rand_word + ' '
        remaining = length - len(pattern)

    # Get rid of trailing space
    pattern = pattern[:length]
    return pattern

if __name__ == '__main__':
    main()
