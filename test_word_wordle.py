from wordle_solver import WordleSolver
from utils import create_dicc_words, create_all_words_test, simulate_game,prints_most_used_words
import time

words_used = {}

dicc_wordle = create_dicc_words()


start = time.time()
solver_wordler = WordleSolver(dicc_wordle)


word_true = "capas"

guesses_words = []
correct = False
for i in range(6):

    game_state = simulate_game(word_true, guesses_words)

    word = solver_wordler.guess_word(game_state, debug=True)
    print(word)
    if word in words_used.keys():
        words_used[word]+=1
    else:
        words_used[word]=1

    guesses_words.append(word)

    if word == word_true:
        correct = True
        break

end = time.time()
print("time to solve: %f"%(end-start))
