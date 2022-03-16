import unicodedata
import os
import sys
import csv

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


def has_numbers(input_string):
     return any(char.isdigit() for char in input_string)

def has_avoid_letters(avoid_letters,input_string):
    return any(char in input_string for char in avoid_letters)

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


def create_words_txt_from_csv(words_length = 5, avoid_letters = [],avoid_words = []):

    words = []
    with open('rae_words.csv') as csv_file:
        
        csv_reader = csv.reader(csv_file, delimiter=',')
        
        next(csv_reader)
        for row in csv_reader:

            if len(row[0])==words_length and " " not in row[0] and not has_numbers(row[0]) and not has_avoid_letters(avoid_letters,row[0]):
                
                
                word = row[0]
                
                word = word.strip()
                word = word.lower()
                word = word.replace("ñ", "#").replace("Ñ", "%")
                word = unicodedata.normalize("NFKD", word)\
                    .encode("ascii", "ignore").decode("ascii")\
                    .replace("#", "ñ").replace("%", "Ñ")

                if word not in words and not word in avoid_words:

                    words.append(word)


    with open(f'palabras_{words_length}_letras.txt', 'w') as f:
        f.write('\n'.join(words))





def create_words_list_from_txt(words_txt,avoid_letters = [],avoid_words = []):

    words = []
    with open(resource_path(words_txt), 'r') as file:

        for word in file:

            word = word.strip()
            word = word.lower()
            word = word.replace("ñ", "#").replace("Ñ", "%")
            word = unicodedata.normalize("NFKD", word)\
                .encode("ascii", "ignore").decode("ascii")\
                .replace("#", "ñ").replace("%", "Ñ")
            
            if  not has_avoid_letters(avoid_letters,word) and word not in avoid_words:

                words.append(word)

    words = list(set(words))
    return words


def prints_most_used_words(words_dicc,th = 5):
    for word in words_dicc.keys():
        if words_dicc[word]>th:
            print("%s : %d"%(word,words_dicc[word]))
