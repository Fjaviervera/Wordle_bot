from wordle_solver import WordleSolver
from utils import create_dicc_words, create_all_words_test, simulate_game,prints_most_used_words

from random import shuffle
import time



correct_words = []
fail_words = []

# all_words = create_all_words_test()
# shuffle(all_words)

all_words = ['vahar', 'havar', 'fizas', 'fogar', 'capas', 'pavas', 'salso', 'faces', 'rajar', 'hayas', 'sisas', 'fabas', 'bisas', 'sajes', 'fajar', 'sabas', 'chaco', 'sallo', 'ahoyo', 'sexas', 'ajoro', 'peñas', 'caces', 'rayar', 'gayes', 'fajas', 'ajara', 'nanga', 'bofas', 'fañar']





words_used = {}


dicc_wordle = create_dicc_words()

for n, word_true in enumerate(all_words):
    start = time.time()
    print("%d/%d" % (n+1, len(all_words)))
    solver_wordler = WordleSolver(dicc_wordle, mode="slow")
    print(word_true)
    guesses_words = []
    correct = False
    for i in range(6):

        game_state = simulate_game(word_true, guesses_words)

        word = solver_wordler.guess_word(game_state, debug=False)

        if word in words_used.keys():
            words_used[word]+=1
        else:
            words_used[word]=1

        guesses_words.append(word)

        if word == word_true:
            correct = True
            break

    if correct:
        correct_words.append(word_true)
    else:
        fail_words.append(word_true)

    end = time.time()
    print("time to solve: %f"%(end-start))


    # prints_most_used_words(words_used)
    print("correct words: %d" % (len(correct_words)))
    print("failed words: %d" % (len(fail_words)))
    print(fail_words)
