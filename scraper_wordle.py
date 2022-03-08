from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from utils import resource_path






def open_game(url):



    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option("detach", True)
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    

    browser = webdriver.Chrome(resource_path("chromedriver_win32/chromedriver.exe"), options=options)
    
    browser.get(url)
    return browser


def send_word(word, browser):

    actions = ActionChains(browser)
    actions.send_keys(word)

    actions.perform()

    actions = ActionChains(browser)
    actions.send_keys(Keys.RETURN)

    actions.perform()


def start(browser):

    start_button = browser.find_elements(
        By.XPATH, "//button[@class='bg-correct text-white active:bg-correct font-bold uppercase text-sm px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1 ease-linear transition-all duration-150']")
    ActionChains(browser).click(start_button[0]).perform()


def send_word_using_screen_board(word, browser):

    keys_button = browser.find_elements(By.XPATH, "//button")
    keyboard = {}
    for key_button in keys_button:
        keyboard[key_button.text.lower()] = key_button

    for letter in word:
        ActionChains(browser).click(keyboard[letter]).perform()
    ActionChains(browser).click(keyboard["enviar"]).perform()


def read_game_custom(browser):

    game_html = browser.find_elements(
        By.XPATH, "//div[@class='flex justify-center mb-1']/div")

    game_state = {"with_position": [], "presents": [], "not_presents": []}
    for index_words in range(0, len(game_html), 5):
        #  0 is grey
        #  1 is yellow
        #  2 is green
        row = {"boxes": [], "green_letters": {}, "yellow_letters": {}}

        for index, letter_html in enumerate(game_html[index_words:index_words + 5]):
            letter_box = {}

            if letter_html.text != "":
                letter_box["letter"] = letter_html.text.lower()

                if letter_box["letter"] not in row["green_letters"].keys():
                    row["green_letters"][letter_box["letter"]] = 0
                if letter_box["letter"] not in row["yellow_letters"].keys():
                    row["yellow_letters"][letter_box["letter"]] = 0

                if "yellow" in letter_html.get_attribute("class"):
                    letter_box["state"] = 1
                    row["yellow_letters"][letter_box["letter"]] += 1

                elif "green" in letter_html.get_attribute("class"):
                    letter_box["state"] = 2
                    row["green_letters"][letter_box["letter"]] += 1

                else:
                    letter_box["state"] = 0

                letter_box["index"] = str(index)
                row["boxes"].append(letter_box)

        game_state = update_game_state(row, game_state)

    return game_state


def read_game_daily(browser):

    game_html = browser.find_elements(
        By.XPATH, "//div[@class='react-card-back']/div")

    game_state = {"with_position": [], "presents": [], "not_presents": []}
    for index_words in range(0, len(game_html), 5):
        #  0 is grey
        #  1 is yellow
        #  2 is green
        row = {"boxes": [], "green_letters": {}, "yellow_letters": {}}

        for index, letter_html in enumerate(game_html[index_words:index_words + 5]):
            letter_box = {}

            if letter_html.text != "":
                letter_box["letter"] = letter_html.text.lower()
                if letter_box["letter"] not in row["green_letters"].keys():
                    row["green_letters"][letter_box["letter"]] = 0
                if letter_box["letter"] not in row["yellow_letters"].keys():
                    row["yellow_letters"][letter_box["letter"]] = 0

                if "bg-present" in letter_html.get_attribute("class"):
                    letter_box["state"] = 1
                    row["yellow_letters"][letter_box["letter"]] += 1

                elif "bg-correct" in letter_html.get_attribute("class"):
                    letter_box["state"] = 2
                    row["green_letters"][letter_box["letter"]] += 1

                else:
                    letter_box["state"] = 0

                letter_box["index"] = str(index)
                row["boxes"].append(letter_box)

        game_state = update_game_state(row, game_state)

    return game_state


def update_game_state(game_row, game_state):

    list_definitive_letters = []
    for letter_box in game_row["boxes"]:

        if letter_box["state"] == 0 and game_row["green_letters"][letter_box["letter"]] > 0:

            list_definitive_letters.append(letter_box["letter"])
            if letter_box["letter"] in game_state["presents"]:
                game_state["presents"].remove(letter_box["letter"])
            for pos in range(5):
                if letter_box["letter"] + str(pos) not in game_state["not_presents"] and letter_box["letter"] + str(pos) not in game_state["with_position"]:
                    game_state["not_presents"].append(
                        letter_box["letter"] + str(pos))

        elif letter_box["state"] == 2:
            if letter_box["letter"] + letter_box["index"] not in game_state["with_position"]:
                game_state["with_position"].append(
                    letter_box["letter"] + letter_box["index"])

            if letter_box["letter"] + letter_box["index"] in game_state["not_presents"]:
                game_state["not_presents"].remove(
                    letter_box["letter"] + letter_box["index"])
            if letter_box["letter"] not in game_state["presents"] and letter_box["letter"] not in list_definitive_letters:
                game_state["presents"].append(letter_box["letter"])

        elif letter_box["state"] == 1:

            if letter_box["letter"] not in game_state["presents"] and letter_box["letter"] not in list_definitive_letters:
                game_state["presents"].append(letter_box["letter"])

            if letter_box["letter"] + letter_box["index"] not in game_state["not_presents"]:
                game_state["not_presents"].append(
                    letter_box["letter"] + letter_box["index"])

        elif letter_box["state"] == 0 and letter_box["letter"] not in game_state["not_presents"] and game_row["yellow_letters"][letter_box["letter"]] == 0:
            game_state["not_presents"].append(letter_box["letter"])

    return game_state
