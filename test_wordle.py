from wordle_solver import WorldeSolver
from utils import create_dicc_words, create_all_words_test, simulate_game

from random import shuffle

correct_words = []
fail_words = []

all_words = create_all_words_test()
shuffle(all_words)


dicc_wordle = create_dicc_words()

for n, word_true in enumerate(all_words):
    print("%d/%d" % (n+1, len(all_words)))
    solver_wordler = WorldeSolver(dicc_wordle)
    print(word_true)
    guesses_words = []
    correct = False
    for i in range(6):

        game_state = simulate_game(word_true, guesses_words)

        word = solver_wordler.guess_word(game_state, debug=False)

        guesses_words.append(word)

        if word == word_true:
            correct = True
            break

    if correct:
        correct_words.append(word_true)
    else:
        fail_words.append(word_true)

    print("correct words: %d" % (len(correct_words)))
    print("failed words: %d" % (len(fail_words)))
    print(fail_words)
