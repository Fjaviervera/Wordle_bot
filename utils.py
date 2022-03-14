import unicodedata
import os
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

def simulate_game(true_word, tried_words):

    game_state = {"with_position": [], "presents": [], "not_presents": []}

    for tried_word in (tried_words):
        row = []
        green_dicc_letters = {}
        yellow_dicc_letters = {}
        for index, guess_letter in enumerate(tried_word):

            if guess_letter not in green_dicc_letters.keys():
                green_dicc_letters[guess_letter] = 0

            if guess_letter not in yellow_dicc_letters.keys():
                yellow_dicc_letters[guess_letter] = 0

            letter_box = {}
            letter_box["letter"] = guess_letter
            letter_box["index"] = str(index)
            if guess_letter == true_word[index]:
                green_dicc_letters[guess_letter] += 1
                letter_box["state"] = 2
            elif guess_letter in true_word and yellow_dicc_letters[guess_letter] < true_word.count(guess_letter):
                letter_box["state"] = 1
                yellow_dicc_letters[guess_letter] += 1
            else:
                letter_box["state"] = 0

            row.append(letter_box)

        list_definitive_letters = []
        for letter_box in row:

            if letter_box["state"] == 1 and green_dicc_letters[letter_box["letter"]] == true_word.count(letter_box["letter"]):

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

            elif letter_box["state"] == 0 and letter_box["letter"] not in game_state["not_presents"] and yellow_dicc_letters[letter_box["letter"]] == 0:
                game_state["not_presents"].append(letter_box["letter"])

    return game_state


def create_dicc_from_words(list_of_words, len_word=5):
    dicc_words = {}
    for word in list_of_words:

        if(len(word) == len_word):

            word = word.replace("ñ", "#").replace("Ñ", "%")
            word = unicodedata.normalize("NFKD", word)\
                .encode("ascii", "ignore").decode("ascii")\
                .replace("#", "ñ").replace("%", "Ñ")

            for index_letter, letter in enumerate(word):
                if letter not in dicc_words.keys():
                    dicc_words[letter] = []
                    dicc_words[letter].append(word)
                elif word not in dicc_words[letter]:
                    dicc_words[letter].append(word)

                if letter + str(index_letter) not in dicc_words.keys():
                    dicc_words[letter + str(index_letter)] = []
                    dicc_words[letter + str(index_letter)].append(word)
                elif word not in dicc_words[letter + str(index_letter)]:
                    dicc_words[letter + str(index_letter)].append(word)

    return dicc_words


def union_lists(list_of_words):

    return set.union(*[set(item) for item in list_of_words])


def intersect_lists(list_of_words):

    intersection_set = set(list_of_words[0])
    for i in range(1, len(list_of_words)):
        intersection_set.intersection_update(set(list_of_words[i]))

    return list(intersection_set)


def difference_lists(possible_words, list_of_words):

    possible_words = set(possible_words)
    for i in range(len(list_of_words)):
        possible_words.difference_update(set(list_of_words[i]))

    return list(possible_words)


def order_list_using_ref(list_to_order, ref):

    zipped_lists = zip(ref, list_to_order)
    sorted_zipped_lists = sorted(zipped_lists, reverse=True)
    ordered_list = [element for _, element in sorted_zipped_lists]

    return ordered_list


def create_dicc_words(avoid_letters=[], avoid_words=[]):

    dicc_wordle = {}

    with open(resource_path("palabras_5_letras.txt"), 'r',encoding="utf8") as file:

        for word in file:

            word = word.strip()
            word = word.lower()
            word = word.replace("ñ", "#").replace("Ñ", "%")
            word = unicodedata.normalize("NFKD", word)\
                .encode("ascii", "ignore").decode("ascii")\
                .replace("#", "ñ").replace("%", "Ñ")

            for avoid_letter in avoid_letters:
                if avoid_letter in word:
                    avoid_words.append(word)

            if word in avoid_words:
                continue

            for index_letter, letter in enumerate(word):
                if letter not in dicc_wordle.keys():
                    dicc_wordle[letter] = []
                    dicc_wordle[letter].append(word)
                else:
                    dicc_wordle[letter].append(word)

                if letter + str(index_letter) not in dicc_wordle.keys():
                    dicc_wordle[letter + str(index_letter)] = []
                    dicc_wordle[letter + str(index_letter)].append(word)
                else:
                    dicc_wordle[letter + str(index_letter)].append(word)

    for key in dicc_wordle.keys():
        dicc_wordle[key] = list(set(dicc_wordle[key]))

    return dicc_wordle


def create_all_words_test():

    all_words = []
    with open(resource_path("palabras_5_letras.txt"), 'r') as file:

        for word in file:

            word = word.strip()
            word = word.lower()
            word = word.replace("ñ", "#").replace("Ñ", "%")
            word = unicodedata.normalize("NFKD", word)\
                .encode("ascii", "ignore").decode("ascii")\
                .replace("#", "ñ").replace("%", "Ñ")

            all_words.append(word)
    all_words = list(set(all_words))
    return all_words


def prints_most_used_words(words_dicc,th = 5):
    for word in words_dicc.keys():
        if words_dicc[word]>th:
            print("%s : %d"%(word,words_dicc[word]))
