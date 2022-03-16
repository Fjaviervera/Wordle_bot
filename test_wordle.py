from wordle_solver import WordleSolver
from utils import create_words_list_from_txt, simulate_game,prints_most_used_words

from random import shuffle
import time



correct_words = []
fail_words = []

all_words = create_words_list_from_txt("words_5_letters.txt")
shuffle(all_words)


words_used = {}



for n, word_true in enumerate(all_words):
    start = time.time()
    print("%d/%d" % (n+1, len(all_words)))
    solver_wordler = WordleSolver(all_words, mode="fast",only2_vowels=True)
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
