from pathlib import Path
from struct import pack
import re
from os import utime
from typing import Union, List, Optional
from string_encoder import encode_string
from reader import read_lte, read_tin, read_re
from datetime import datetime

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
    def __init__(self, name: str, director: str, location: str, date: Optional[str]=None) -> None:
        self.name = name
        self.director = director
        self.location = location
        if date is None:
            self.date = None
        else:
            self.date = datetime.strptime(date, format='%d/%m/%Y').timestamp()
        self.num_rounds = None
        self.players = []
        self.games = []
        self.current_round = 0

    def read_from_scrabble_manager(self, filepath: Union[str, Path]) -> None:
        fpath_no_suffix = str(Path(filepath).parent / Path(filepath).stem)
        players = read_lte(fpath_no_suffix + '.lte')
        for i, (name, town, rating) in enumerate(players):
            name_with_comma = f'{name.split()[-1]}, {name.split()[:-1]}'
            new_player = Player(i+1, name_with_comma, rating, town)
            self.players.append(new_player)

        _, self.num_rounds, _ = read_tin(fpath_no_suffix + '.tin')
        games = read_re(fpath_no_suffix + '.re')
        for i, (state, board, result, score, opponent) in enumerate(games[:-3]):
            player_id = i // (self.num_rounds+1) + 1
            round_no = i % (self.num_rounds+1) + 1
            if round_no == self.num_rounds+1:
                continue
            if opponent == 0:
                self.games.append(Game(round_no, board=0, id1=player_id, score1=score))
            elif opponent > player_id:
                if state == 1:
                    self.games.append(Game(round_no, board, id1=player_id, score1=score, id2=opponent))
                elif state == 2:
                    self.games.append(Game(round_no, board, id1=opponent, id2=player_id, score2=score))
            else:
                for game in self.games:
                    if game.round == round_no and game.board == board:
                        if state == 1:
                            assert game.player1 == player_id
                            assert game.player2 == opponent
                            assert game.score1 is None
                            game.score1 = score
                        else:
                            assert game.player2 == player_id
                            assert game.player1 == opponent
                            assert game.score2 is None
                            game.score2 = score

    def read_from_t(self, filepath: Union[str, Path]) -> None:
        re_name = re.compile('(.*?)([0-9].*)')
        with open(filepath) as f:
            player_id = 1
            for line in f:
                re_split_line = re.search(re_name, line)
                fields = re_split_line.group(2).split(';')
                print(fields)
                rating_and_opponents = fields.pop(0).split()
                name = re_split_line.group(1).strip()
                rating = rating_and_opponents[0]

                if self.date is None:
                    rtime_field = 0
                    for field in fields:
                        if field.startswith(' rtime'):
                            break
                        rtime_field += 1
                    rtimes = fields.pop(rtime_field)[7:].split()
                    self.date = int(rtimes[0])

                team_field = 0
                for field in fields:
                    if field.startswith(' TEAM'):
                        break
                    team_field += 1
                team = fields.pop(team_field)[5:].strip()
                new_player = Player(player_id, name, float(rating), team)
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
                assert len(scores) == len(opponents) == len(boards) == len(who_first_list)
                round_no = 1
                for score, opponent, board, who_first in zip(scores, opponents, boards, who_first_list):
                    if self.num_rounds is None:
                        self.num_rounds = round_no
                    elif round_no > self.num_rounds:
                        self.num_rounds = round_no

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
                    round_no += 1

                player_id += 1

    def export_nag(self, output_filename: Union[str, Path]) -> None:
        with open(output_filename, 'wb') as f:
            f.write(encode_string(self.name))

    def export_lte(self, output_filename: Union[str, Path]) -> None:
        with open(output_filename, 'wb') as f:
            for player in self.players:
                name = f'{player.first_name} {player.last_name}'
                player_desc = f'{name: <36}{player.rating: <6.2f}{player.team: <25}'
                f.write(encode_string(player_desc))

    def export_tin(self, output_filename: Union[str, Path]) -> None:
        num_players = len(self.players)
        player_numbers = list(i+1 for i in range(num_players))
        with open(output_filename, 'wb') as f:
            f.write(pack('=H', num_players))
            f.write(pack('=H', self.num_rounds))
            f.write(pack('=H', 0))  # nWakat
            f.write(pack('=7H', 0, 0, 0, 0, 0, 0, 0))
            f.write(pack(f'={num_players}H', *player_numbers))
            f.write(pack('=2H', 1, 3))
        utime(output_filename, times=(self.date, self.date))

    def export_re(self, output_filename: Union[str, Path]) -> None:
        struct_fmt = '=bBHHH'
        with open(output_filename, 'wb') as f:
            for player in self.players:
                games = self.get_players_games(player.id)
                for game in games:
                    result = None
                    board = game.board
                    if game.score1 == game.score2:  # draw
                        result = 1
                    if game.player2 is None and game.score2 is None:
                        if game.score1 == 0:  # did not play
                            result = 0
                            state = 0
                        else:  # BYE
                            board = self.find_last_board_number(game.round) + 1
                            result = 2  # not sure why BYE result is the same as win result
                            state = 3
                    else:
                        state = 1 if player.id == game.player1 else 2
                    if player.id == game.player1:
                        score = game.score1
                        opponent = game.player2 or 0
                        if result is None:
                            result = 2*int(game.score1 > game.score2)
                    else:
                        score = game.score2
                        opponent = game.player1 or 0
                        if result is None:
                            result = 2*int(game.score2 > game.score1)

                    struct_packed = pack(struct_fmt, state, board, result, score, opponent)
                    f.write(struct_packed)
                last_game = pack(struct_fmt, 0, 0, 32767, 32767, 0)
                f.write(last_game)
            last_three = pack(struct_fmt, 1, 0, self.num_rounds + 1, 32767, 0)
            for i in range(3):
                f.write(last_three)

    def export_smt(self, output_filename: Union[str, Path]) -> None:
        midnight_today = datetime.fromtimestamp(self.date)
        days_from_1900 = (midnight_today - datetime(1899, 12, 30, 0, 0)).days
        days_str = f'{days_from_1900:.6f}'
        with open(output_filename, 'wb') as f:
            f.write(bytes(days_str, 'ascii'))
            f.write(b'\r\n')
            f.write(bytes(self.location, 'cp1250'))
            f.write(b'\r\n')
            f.write(bytes(self.director, 'cp1250'))
            f.write(b'\r\n')
            f.write(b'1\r\n1\r\n0\r\n1\r\n3\r\n')
            for r in range(self.num_rounds-1):
                f.write(bytes(f'{r+1} 1', 'ascii'))
                f.write(b'\r\n')
            f.write(bytes(f'{self.num_rounds} 3', 'ascii'))
            f.write(b'\r\n')
            for p in range(len(self.players)):
                f.write(bytes(f'{p+1} 0.000 0 1', 'ascii'))
                f.write(b'\r\n')

    def find_last_board_number(self, round_no: int) -> int:
        games_list = [g for g in self.games if g.round == round_no]
        max_board = 0
        for game in games_list:
            max_board = max(game.board, max_board)
        return max_board

    def get_players_games(self, player_id: int) -> List[Game]:
        games_list = [g for g in self.games if g.player1 == player_id or g.player2 == player_id]
        return sorted(games_list, key=lambda x: x.round)


class Player(object):
    def __init__(self, id: int, name: str, rating: Optional[float]=None,
                 team: Optional[str]=None) -> None:
        self.id = id
        self.name = name
        name_split = self.name.split(',')
        self.first_name = name_split[1].strip()
        self.last_name = name_split[0].strip()
        self.rating = rating
        self.team = '' if team is None else team

    def __repr__(self) -> str:
        return f'{self.first_name} {self.last_name}\t{self.team}\t{self.rating}'


tour = Tournament('Mistrzostwa TSH', 'Adam Kłimónt', 'Cambridge')
tour.read_from_t('/home/adam/code/tsh/samplepl/a.t')
tour.export_re('/home/adam/Downloads/test.re')
tour.export_tin('/home/adam/Downloads/test.tin')
tour.export_lte('/home/adam/Downloads/test.lte')
tour.export_nag('/home/adam/Downloads/test.nag')
tour.export_smt('/home/adam/Downloads/test.smt')
games = tour.get_players_games(8)

print(games)
# for g in tour.games:
#     print(g)
for p in tour.players:
    print(p)

newtour = Tournament('Poznań', 'Grzegorz', 'Poznań')
newtour.read_from_scrabble_manager('/home/adam/Downloads/Poznan_2018_export/poznan.re')
for g in newtour.games:
    print(g)