import copy
from collections import Counter

class RiichiUtils:
    numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    splitters = ["m", "s", "p", "d", "w"]
    valid_characters = splitters + numbers + ["!"]

    github_dict = {
        "colours": {
            "m": "Man",
            "p": "Pin",
            "s": "Sou",
            "d": "Dragon",
            "w": "Wind"
        },
        "dragons": {
            "1": "Haku",  # white
            "2": "Hatsu",  # green
            "3": "Chun"  # red
        },
        "winds": {
            "1": "Ton",  # east
            "2": "Nan",  # south
            "3": "Shaa",  # west
            "4": "Pei"  # north
        }
    }

    @classmethod
    def split_tiles(cls, colour_list: list) -> list:
        output_list = []
        for idx, i in enumerate(reversed(colour_list)):
            output_list.append(i.replace(colour_list[len(colour_list) - idx - 2], ""))
        return output_list

    @classmethod
    def how_many_kans(cls, tile_dict: dict) -> int:
        kan_amount = 0
        # and if i dont do this it removes the dora tiles from the hand because dictionaries get edited globally xdddddd
        copy_dict = copy.deepcopy(tile_dict)
        for k, v in copy_dict.items():
            for idx, i in enumerate(v):
                # insane edge case: dora tiles don't count towards kan xD
                if i == "5!":
                    v[idx] = "5"
            tile_counts = Counter(v)
            for tile, count in tile_counts.items():
                if count > 4:
                    raise RiichiError(f"there are only a maximum of 4 copies of a tile.")
                elif count == 4:
                    kan_amount += 1
        return kan_amount

    @classmethod
    def handle_riichi_hand_errors(cls, hand_string: str) -> dict:
        number_count = 0
        akadora_found = False
        for idx, i in enumerate(hand_string):
            # irrelevant characters
            if i not in cls.valid_characters:
                raise RiichiError(f"this character: \"{i}\" is not correct notation!")
            # akadora stuff
            if i == "!":
                # akadora indicator not after a number
                if hand_string[idx - 1] not in cls.numbers:
                    raise RiichiError(f"please only use akadora indicators (\'!\') after numbers! problem: \"{hand_string[idx - 1] + i}\" in hand: {hand_string}")
                # dora indicator on anything but a 5
                elif hand_string[idx - 1] != "5":
                    raise RiichiError(f"only \"5\" tiles can be akadora tiles. problem: \"{hand_string[idx - 1] + i}\" in hand: {hand_string}")
                if not akadora_found:
                    akadora_found = True
                else:
                    raise RiichiError(f"there can only be one akadora per colour! hand: {hand_string}")

            if i in cls.splitters and hand_string[idx - 1] in cls.splitters:
                raise RiichiError(f"please do not use empty colours! just don't include the splitter if you don't have any. problem: \"{hand_string[idx - 1] + i}\" in hand: {hand_string}")

            if i in cls.numbers:
                number_count += 1
            elif i in cls.splitters:
                akadora_found = False
        # hand doesn't end with a splitter
        if list(reversed(hand_string))[0] in cls.numbers:
            raise RiichiError(f"your hand is invalid! it needs to end with a splitter ({', '.join(cls.splitters)}).")

        # splitters used more than once
        for c in cls.splitters:
            if c in hand_string:
                if hand_string.count(c) > 1 or hand_string.count(c) > 5:
                    raise RiichiError(f"please only put each splitter ({', '.join(cls.splitters)}) once!")

        # for tile based inconsistencies
        tiles = cls.separate_into_colours(hand_string)
        # too many tiles, but have to check for kans
        amount_of_kans_in_hand = cls.how_many_kans(tiles)
        max_allowed_tiles = 14 + amount_of_kans_in_hand
        if number_count > max_allowed_tiles:
            raise RiichiError(f"riichi hands can only have a maximum of {max_allowed_tiles}"
                              f" {'(14 default + ' + str(amount_of_kans_in_hand) + ' from ' + str(amount_of_kans_in_hand) +' kan(s))' if amount_of_kans_in_hand > 0 else ''}"
                              f" tiles. yours has {number_count}.")
        # self explanatory
        for k, v in tiles.items():
            if k in ("d", "w") and "!" in "".join(v):
                raise RiichiError(f"there can be no red dora tiles for dragons or winds!")
            if k == "d" and not all(int(x) <= 3 for x in v):
                raise RiichiError(f"there are no dragon tiles higher than 3.")
            if k == "w" and not all(int(x) <= 4 for x in v):
                raise RiichiError(f"there are no wind tiles higher than 4.")
            for n in cls.numbers:
                if v.count(n) > 4:
                    raise RiichiError(f"there are only a maximum of 4 copies of a tile. problem: \"{n*v.count(n)+k}\" (this is a failsafe and should never happen)")
        return tiles

    @classmethod
    def separate_into_colours(cls, hand_string: str) -> dict:
        tiles: dict = {}
        current_colour = []
        for character in hand_string:
            if character in cls.numbers:
                current_colour.append(character)
            elif character == "!":
                current_colour[len(current_colour) - 1] = current_colour[len(current_colour) - 1] + "!"
            elif character in cls.splitters:
                tiles[character] = current_colour
                current_colour = []
        return tiles

    @classmethod
    def get_github_names(cls, tile_dict: dict) -> list:
        github_list = []
        for k, v in tile_dict.items():
            current_colour: str = cls.github_dict["colours"][k]
            if current_colour in ("Man", "Pin", "Sou"):
                for tile in v:
                    to_append = current_colour+tile
                    if "!" in tile:
                        to_append = to_append[:-1]
                        to_append += "-Dora"
                    github_list.append(to_append)
            elif current_colour == "Dragon":
                for tile in v:
                    github_list.append(cls.github_dict["dragons"][tile])
            elif current_colour == "Wind":
                for tile in v:
                    github_list.append(cls.github_dict["winds"][tile])
        return github_list

    @classmethod
    def get_links_from_github_list(cls, github_list):
        base_link = "https://raw.githubusercontent.com/FluffyStuff/riichi-mahjong-tiles/refs/heads/master/Regular/{}.svg"
        link_list = []  # lol linked list xd
        for tile in github_list:
            link_list.append(base_link.format(tile))
        return link_list

    @classmethod
    def sort_hand_tiles(cls, hand_tiles: dict) -> dict:
        copy_dict = copy.deepcopy(hand_tiles)
        for k, v in copy_dict.items():
            copy_dict[k] = sorted(v)
        return copy_dict

class RiichiError(Exception):
    pass
