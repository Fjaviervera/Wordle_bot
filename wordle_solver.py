from utils import *

import multiprocessing
from joblib import Parallel, delayed


num_cores = multiprocessing.cpu_count()



class WordleSolver():

    def __init__(self, words_list,mode = "fast",parallel_sim = True, only2_vowels = False):
        

        self.words_length = len(words_list[0])
        self.generate_dicc_from_list(words_list)
        self.parallel_sim = parallel_sim
        self.words_tested = []
        self.possible_words_to_fish = self.get_possible_words(
            {"with_position": [], "presents": [], "not_presents": []}, only2_vowels)

        if mode == "slow":
            self._th_to_simulate = [1000,100]
            self._n_to_rank = [100,200]
        elif mode == "ultra-slow":
            self._th_to_simulate = [1000,100]
            self._n_to_rank = [500,1000]
        elif mode == "fast":
            self._th_to_simulate = [1000,100]
            self._n_to_rank = [20,100]
        else:
            print("Unrecognized mode, using fast")
            self._th_to_simulate = [1000,100]
            self._n_to_rank = [20,100]
    
    def generate_dicc_from_list(self,words_list):
        
        self.words_dicc = {}

        for word in words_list:

            word = word.strip()
            word = word.lower()
            word = word.replace("ñ", "#").replace("Ñ", "%")
            word = unicodedata.normalize("NFKD", word)\
                .encode("ascii", "ignore").decode("ascii")\
                .replace("#", "ñ").replace("%", "Ñ")


            for index_letter, letter in enumerate(word):
                if letter not in self.words_dicc.keys():
                    self.words_dicc[letter] = []
                    self.words_dicc[letter].append(word)
                else:
                    self.words_dicc[letter].append(word)

                if letter + str(index_letter) not in self.words_dicc.keys():
                    self.words_dicc[letter + str(index_letter)] = []
                    self.words_dicc[letter + str(index_letter)].append(word)
                else:
                    self.words_dicc[letter + str(index_letter)].append(word)

        for key in self.words_dicc.keys():
            self.words_dicc[key] = list(set(self.words_dicc[key]))


    def check_correct_word(self, game_state):
        if len(game_state["with_position"]) == self.words_length:
            return True
        else:
            return False

    def get_possible_words_to_fish(self):
        return self.possible_words_to_fish

    def get_possible_words(self, game_state, only2_vowels = False):

        list_words = []
        not_list_words = []

        for letterPos in game_state["with_position"]:
            list_words.append(self.words_dicc[letterPos])
        for letter in game_state["presents"]:
            list_words.append(self.words_dicc[letter])
        for not_letter in game_state["not_presents"]:
            if not_letter in self.words_dicc.keys():
                not_list_words.append(self.words_dicc[not_letter])
        if len(list_words) > 0:
            possible_words = intersect_lists(list_words)
            possible_words = difference_lists(possible_words, not_list_words)
        else:
            words_reamining = []
            for letter in self.words_dicc.keys():
                if letter not in game_state["not_presents"]:
                    words_reamining.append(self.words_dicc[letter])
            possible_words = union_lists(words_reamining)
            possible_words = difference_lists(possible_words, not_list_words)

        if only2_vowels:
            possible_words_vocals = []
            vocals = ["a", "e", "i" , "o" , "u"]
            for word in possible_words:
                vocals_n = 0
                for letter  in word:
                    if letter in vocals:
                        vocals_n+=1
                if vocals_n<2:
                    possible_words_vocals.append(word)

            possible_words = possible_words_vocals

        return possible_words

    def get_most_possible_words_to_fish(self, word_list, avoid_letters=[]):
        
        words_dicc = create_dicc_from_words(word_list, len_word=self.words_length )
        dicc_count_letters = {}
        for letter in words_dicc.keys():


            if len(letter) == 1 and letter not in avoid_letters:

                dicc_count_letters[letter] = len(words_dicc[letter])
            elif len(letter) == 2:
                dicc_count_letters[letter] = len(words_dicc[letter])

        letter_count_in_possible_words = []

        for index in range(len(self.possible_words_to_fish)):
            letter_count = 0
            letters_counted = []
            for pos,letter in enumerate(self.possible_words_to_fish[index]):
                if letter in dicc_count_letters.keys():
                    if letter not in letters_counted:
                        letters_counted.append(letter)
                        letter_count += dicc_count_letters[letter]
                    if letter + str(pos)   in dicc_count_letters.keys():
                        letter_count += dicc_count_letters[letter+ str(pos)]
            letter_count_in_possible_words.append(letter_count)


        return order_list_using_ref(self.possible_words_to_fish, letter_count_in_possible_words)

    def simulate_round_game(self,results,candidate,target,num_possible_words):

        guesses_words = self.words_tested + [candidate]

        game_state = simulate_game(target, guesses_words)

        possible_words_simulation = self.get_possible_words(game_state)

        results += num_possible_words - len(possible_words_simulation)
        return results

    def simulate_candidate(self,candidate,possible_words):
        results = 0

        for target in possible_words:

            results = self.simulate_round_game(results,candidate,target,len(possible_words))

        return results

    def simulate_most_possible_words_to_fish_parallel(self, possible_words_to_fish, possible_words, ranking):


        list_candidates_results = Parallel(n_jobs=num_cores)(delayed(self.simulate_candidate)(candidate,possible_words) 
                                                        for candidate in possible_words_to_fish[0:ranking])

        words_ranked = order_list_using_ref(
            possible_words_to_fish[0:ranking], list_candidates_results)

        return words_ranked


    def simulate_most_possible_words_to_fish(self, possible_words_to_fish, possible_words, ranking):

        list_candidates_results = []

        for candidate in possible_words_to_fish[0:ranking]:
            results = 0

            for target in possible_words:

                guesses_words = self.words_tested + [candidate]

                game_state = simulate_game(target, guesses_words)

                possible_words_simulation = self.get_possible_words(game_state)

                results += len(possible_words) - len(possible_words_simulation)

            list_candidates_results.append(results)

        words_ranked = order_list_using_ref(
            possible_words_to_fish[0:ranking], list_candidates_results)

        return words_ranked



    def guess_word(self, game_state, debug=False):

        possible_words = self.get_possible_words(game_state)

        possible_words = list(set(possible_words))

        if debug:
            print(game_state)
            print(len(possible_words))
            if len(possible_words) < 15:
                print(possible_words)

        if len(possible_words) > 0:

            if len(possible_words) > 1:

                all_words_same_letters = all(set(word) == set(
                    possible_words[0]) for word in possible_words)

                letters_to_avoid_count = []

                if not all_words_same_letters:

                    for letter in game_state["with_position"]:
                        letters_to_avoid_count.append(letter[0])
                    for letter in game_state["presents"]:
                        if letter not in letters_to_avoid_count:
                            letters_to_avoid_count.append(letter)

                    if len(possible_words) < 20:
                        shared_letters = intersect_lists(possible_words)
                        for letter in list(shared_letters):
                            if letter not in letters_to_avoid_count:
                                letters_to_avoid_count += letter

                possible_words_to_fish = self.get_most_possible_words_to_fish(
                    possible_words, letters_to_avoid_count)

                if len(possible_words) < self._th_to_simulate[0]:
                    
                    if len(possible_words)<self._th_to_simulate[1]: 
                        rank = self._n_to_rank[1]
                    else:
                        rank = self._n_to_rank[0]

                    if self.parallel_sim:
                        possible_words_to_fish = self.simulate_most_possible_words_to_fish_parallel(
                            possible_words_to_fish, possible_words, ranking=rank)
                    else:
                        possible_words_to_fish = self.simulate_most_possible_words_to_fish(
                            possible_words_to_fish, possible_words, ranking=rank)

               



                for word in possible_words_to_fish:
                    if word in self.words_tested:
                        continue

                    else:
                        self.words_tested.append(word)

                        return word
            else:
                return possible_words[0]

        else:
            print("fail no possible words available")
