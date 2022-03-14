from time import sleep
from wordle_solver import WordleSolver
import scraper_wordle
from utils import create_dicc_words



WORDLE_CUSTOM = "https://mywordle.strivemath.com/?word=rsvup&lang=sp"

WORDLE_DAILY = "https://wordle.danielfrg.com/"


wordle_url = WORDLE_DAILY

browser = scraper_wordle.open_game(wordle_url)
sleep(0.5)

if 'strivemath' not in wordle_url:

    scraper_wordle.start(browser)
    sleep(0.5)
    dicc_wordle = create_dicc_words()
else:
    # custom wordle is not compatible with ñ and some words, probable this isn't all of them
    dicc_wordle = create_dicc_words(avoid_letters=["ñ"], avoid_words=[
                                    "zungo", "vinto", "depto", "putre", "tunja", "tupac"])

solver_wordler = WordleSolver(dicc_wordle)

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

