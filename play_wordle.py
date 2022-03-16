from time import sleep, time
from wordle_solver import WordleSolver
import scraper_wordle
from utils import create_words_list_from_txt



WORDLE_CUSTOM = "https://mywordle.strivemath.com/?word=wqlgz&lang=sp"

WORDLE_DAILY = "https://wordle.danielfrg.com/"


wordle_url = WORDLE_DAILY


browser = scraper_wordle.open_game(wordle_url)
sleep(0.5)
start = time()


if 'strivemath' not in wordle_url:

    scraper_wordle.start(browser)
    sleep(0.5)
    words_list = create_words_list_from_txt("palabras_5_letras.txt",avoid_letters = [],avoid_words = [])
else:
    # custom wordle is not compatible with ñ and some words, probable this isn't all of them
    words_list = create_words_list_from_txt("palabras_5_letras.txt",avoid_letters = ["ñ"],avoid_words = ["zungo", "vinto", "depto", "putre", "tunja", "tupac","gomez","hazte","gafez"])
    
    

solver_wordler = WordleSolver(words_list)

for i in range(6):

    if 'strivemath' in wordle_url:
        game_state = scraper_wordle.read_game_custom(browser)
    else:
        game_state = scraper_wordle.read_game_daily(browser)

    if solver_wordler.check_correct_word(game_state):
        break

    word = solver_wordler.guess_word(game_state, debug=True)

    if 'strivemath' in wordle_url:
        scraper_wordle.send_word(word, browser)
        sleep(0.1)
    else:
        scraper_wordle.send_word_using_screen_board(word, browser)

end = time()
print("time to solve: %f"%(end-start))