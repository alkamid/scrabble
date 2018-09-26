from pathlib import Path
import re
from typing import Union, List


class Game(object):
    def __init__(self, round_no: int, board: int, id1: int, id2: int, score1: int, score2: int, who_first: int) -> None:
        self.round = round_no
        self.board = board
        self.player1 = id1
        self.player2 = id2
        self.score1 = score1
        self.score2 = score2
        if who_first not in (1, 2):
            raise ValueError('Indicate who went first (1 or 2)!')
        self.who_first = who_first



class Tournament(object):
    def __init__(self) -> None:
        self.num_rounds = None
        self.players = []
        self.games = []
        self.current_round = 0

    def read_from_t(self, filepath: Union[str, Path]) -> None:
        re_name = re.compile('(.*?)([0-9].*)')
        with open(filepath) as f:
            for line in f:
                re_split_line = re.search(re_name, line)
                name = re_split_line.group(1).strip()
                fields = re_split_line.group(2).split(';')
                rating_and_scores = fields.pop(0).split()
                rating = rating_and_scores[0]
                scores = rating_and_scores[1:]

                board_field = 0
                for field in fields:
                    if field.startswith(' board'):
                        break
                    board_field += 1
                boards = fields.pop(board_field)[6:]

                who_first_field = 0
                for field in fields:
                    if field.startswith(' p12'):
                        break
                    who_first_field += 1
                who_first_list = fields.pop(who_first_field)[3:]
                print(boards)


    def get_players_games(self, player_id: int) -> List[Game]:
        games_list = [g for g in self.games if g.player1 == player_id or g.player2 == player_id]
        return sorted(games_list, key=lambda x: x.round)


class Player(object):
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name



tour = Tournament()
tour.read_from_t('a.t')
