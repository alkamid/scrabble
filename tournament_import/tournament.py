from pathlib import Path
import re
from typing import Union, List


class Game(object):
    def __init__(self, round_no: int, board: int, id1: int=None, id2: int=None, score1: int=None, score2: int=None) -> None:
        self.round = round_no
        self.board = board
        self.player1 = id1
        self.player2 = id2
        self.score1 = score1
        self.score2 = score2

    def __repr__(self):
        return f'round: {self.round}\tboard: {self.board}\tp1: {self.player1} ({self.score1})\t' \
               f'p2: {self.player2} ({self.score2})'


class Tournament(object):
    def __init__(self) -> None:
        self.num_rounds = None
        self.players = []
        self.games = []
        self.current_round = 0

    def read_from_t(self, filepath: Union[str, Path]) -> None:
        re_name = re.compile('(.*?)([0-9].*)')
        with open(filepath) as f:
            player_id = 1
            for line in f:
                re_split_line = re.search(re_name, line)
                fields = re_split_line.group(2).split(';')
                rating_and_opponents = fields.pop(0).split()
                name = re_split_line.group(1).strip()
                rating = rating_and_opponents[0]
                new_player = Player(player_id, name)
                new_player.rating = float(rating)
                self.players.append(new_player)
                opponents = [int(a) for a in rating_and_opponents[1:]]
                scores = [int(a) for a in fields.pop(0).strip().split()]

                board_field = 0
                for field in fields:
                    if field.startswith(' board'):
                        break
                    board_field += 1
                boards = [int(a) for a in fields.pop(board_field)[6:].strip().split()]

                who_first_field = 0
                for field in fields:
                    if field.startswith(' p12'):
                        break
                    who_first_field += 1
                who_first_list = [int(a) for a in fields.pop(who_first_field)[4:].strip().split()]

                assert all([a == 1 or a == 2 or a == 0 for a in who_first_list])
                print(scores)
                print(opponents)
                print(boards)
                print(who_first_list)
                assert len(scores) == len(opponents) == len(boards) == len(who_first_list)
                round_no = 1
                for score, opponent, board, who_first in zip(scores, opponents, boards, who_first_list):
                    if opponent == 0 and board == 0:
                        self.games.append(Game(round_no, board, id1=player_id, score1=score))
                    elif opponent > player_id:
                        if who_first == 1:
                            new_game = Game(round_no, board, id1=player_id, score1=score)
                        else:
                            new_game = Game(round_no, board, id2=player_id, score2=score)
                        self.games.append(new_game)
                    else:
                        for game in self.games:
                            if game.round == round_no and game.board == board:
                                if who_first == 1:
                                    assert game.player1 is None
                                    assert game.score1 is None
                                    game.player1 = player_id
                                    game.score1 = score
                                else:
                                    assert game.player2 is None
                                    assert game.score2 is None
                                    game.player2 = player_id
                                    game.score2 = score
                    round_no +=1

                player_id += 1

    def export_nag(self, output_filename: Union[str, Path]) -> None:
        raise NotImplementedError

    def export_lte(self, output_filename: Union[str, Path]) -> None:
        raise NotImplementedError

    def export_tin(self, output_filename: Union[str, Path]) -> None:
        raise NotImplementedError

    def export_re(self) -> None:
        raise NotImplementedError

    def get_players_games(self, player_id: int) -> List[Game]:
        games_list = [g for g in self.games if g.player1 == player_id or g.player2 == player_id]
        return sorted(games_list, key=lambda x: x.round)


class Player(object):
    def __init__(self, id, name) -> None:
        self.id = id
        self.name = name
        self.rating = None

    def __repr__(self) -> str:
        name_split = self.name.split(',')
        first_name = name_split[1].strip()
        last_name = name_split[0].strip()
        return f'{first_name} {last_name}\t{self.rating}'



tour = Tournament()
tour.read_from_t('a.t')
for g in tour.games:
    print(g)
for p in tour.players:
    print(p)