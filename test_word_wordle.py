from wordle_solver import WordleSolver
from utils import create_words_list_from_txt,simulate_game
import time

words_used = {}

word_list = create_words_list_from_txt("words_5_letters.txt")


start = time.time()
solver_wordler = WordleSolver(word_list, parallel_sim=True,mode = "dual_sim",only1_vowels=False)

word_true = "jills"

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

