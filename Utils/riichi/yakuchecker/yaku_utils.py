import copy
from collections import Counter

from Utils.riichi.RiichiUtils import RiichiUtils

class YakuUtils:
    @classmethod
    def remove_doras(cls, hand: dict):
        copy_dict = copy.deepcopy(hand)
        for k, v in copy_dict.items():
            for idx, i in enumerate(v):
                if i == "5!":
                    v[idx] = "5"
        return copy_dict

    @classmethod
    def extract_sets(cls, sorted_hand: dict, type: int):
        sorted_hand = YakuUtils.remove_doras(sorted_hand)
        set_list = []
        for colour, tile_list in sorted_hand.items():
            tile_count = Counter(tile_list)
            for tile, amount_of_tile in tile_count.items():
                if type in (2, 4):
                    if amount_of_tile == type:
                        set_list.append((colour, tile))
                elif type == 3:
                    if amount_of_tile >= type:
                        set_list.append((colour, tile))
        return set_list

    @classmethod
    def extract_possible_chis(cls, sorted_hand: dict):
        sorted_hand = YakuUtils.make_all_tiles_unique(YakuUtils.remove_doras(sorted_hand))
        chi_dict = {}
        for colour, tile_list in sorted_hand.items():
            this_colour_chis = []
            if colour in ("w", "d"): continue
            if len(tile_list) < 3: continue
            for idx, tile in enumerate(tile_list):
                a = idx+2, len(tile_list)-1
                if idx+2 > len(tile_list)-1: break
                tile, tile_next, tile_uebernext_leel = tile_list[idx], tile_list[idx+1], tile_list[idx+2]
                if int(tile) == int(tile_next)-1 and int(tile_next) == int(tile_uebernext_leel)-1:
                    this_colour_chis.append((tile, tile_next, tile_uebernext_leel))
            chi_dict[colour] = this_colour_chis
        return chi_dict

    @classmethod
    def _extract_possible_possible_chis_one_colour(cls, haaaaand: list, current_cheese = None):
        if current_cheese is None:
            current_cheese = []

        cheeses = []
        ham_wir_was_gefunden = False

        for tile_index in range(len(haaaaand)):
            tile = haaaaand[tile_index]

            tile2, tile3 = str(int(tile) + 1), str(int(tile) + 2)

            if tile2 in haaaaand and tile3 in haaaaand:
                ham_wir_was_gefunden = True
                uebrige_nigger = haaaaand[:]
                uebrige_nigger.remove(tile)
                uebrige_nigger.remove(tile2)
                uebrige_nigger.remove(tile3)

                manuel_neuer = current_cheese + [(tile, tile2, tile3)]
                cheeses.extend(cls._extract_possible_possible_chis_one_colour(uebrige_nigger, manuel_neuer))

        if not ham_wir_was_gefunden and current_cheese:
            return [current_cheese]
        return cheeses

    @classmethod
    def make_all_tiles_unique(cls, sorted_hand: dict):
        sorted_hand = YakuUtils.remove_doras(sorted_hand)
        new_dict = {}
        for colour, tile_list in sorted_hand.items():
            new_list = []
            for tile in tile_list:
                if tile not in new_list:
                    new_list.append(tile)
                else:
                    continue
            new_dict[colour] = new_list
        return new_dict

    @classmethod
    def extract_possible_possible_chis(cls, hand: dict):
        full_chi_dict = {}
        hand_without_dora = cls.remove_doras(hand)
        for colour, tile_list in hand_without_dora.items():
            chi_list_one_colour = cls._extract_possible_possible_chis_one_colour(tile_list)
            sorted_list = []
            for element in chi_list_one_colour:
                element = sorted(element)
                if element not in sorted_list:
                    sorted_list.append(element)
            full_chi_dict[colour] = sorted_list
        return full_chi_dict

example_hand = "11223344556677m"

if __name__ == "__main__":
    hand_tiles = RiichiUtils.handle_riichi_hand_errors(example_hand)
    nigger = RiichiUtils.sort_hand_tiles(hand_tiles)
    nigger2 = YakuUtils.extract_possible_chis(nigger)
    nigger3 = YakuUtils.extract_possible_possible_chis(nigger)
    print(nigger3)
