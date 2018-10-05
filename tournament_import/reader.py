import struct
from pathlib import Path
from typing import List, Tuple, Union
from string_encoder import decode_string


def read_chunks(f, length):
    while True:
        data = f.read(length)
        if not data:
            break
        yield data


def read_lte(filename: Union[str, Path]) -> List[Tuple[str, str, float]]:
    """
    .lte files contain the list of players. It is initially sorted by rating, then
    latecomers are added to the end of the list. All lines have a fixed width of 67 bytes.
    Args:
        filename:
    Returns:
        List of tuples (name, town/team, rating)
    """
    players = []
    with open(filename, "rb") as f:
        while True:
            player_data = decode_string(f.read(36+6+25))
            if not player_data:
                break
            name = player_data[:36].strip()
            rating = float(player_data[36:42])
            town = player_data[42:].strip()
            players.append((name, town, rating))
    return players


def read_re(filename: Union[str, Path]) -> List[Tuple[int, int, int, int, int]]:
    """
    .re files contain tuples of five numbers:
    - status: 0 - did not play, 1 - went first, 2 - went second, 3 - bye
    - stol (board)
    - wynik (result): presumably 0 for losing, 1 for drawing, 2 for winning, but not used in
    Scrabble Manager import
    - male_pkt (score)
    - nr_przeciwnika (opponent ID): matches the order from .lte files
    Args:
        filename:

    Returns:
        List of tuples of five integers.
    """
    struct_fmt = '=bBHHH'
    struct_len = struct.calcsize(struct_fmt)
    struct_unpack = struct.Struct(struct_fmt).unpack_from

    with open(filename, "rb") as f:
        results = [struct_unpack(chunk) for chunk in read_chunks(f, struct_len)]

    return results


def read_tin(filename: Union[str, Path]) -> Tuple[int, int, Tuple[int, int]]:
    """
    .tin files contain general info about a tournament. Some of the data are unused
    (marked as "bridge rubbish"), some is redundant (number of players can be
    read from .lte, number of rounds from .re), only the last tuple of two flags
    is unique to this file - they specify winning criteria.
    Args:
        filename:

    Returns:

    """
    head_fmt = '=HHH7H'
    head_len = struct.calcsize(head_fmt)
    head_unpack = struct.Struct(head_fmt).unpack_from
    flag_fmt = '=2H'
    flag_len = struct.calcsize(flag_fmt)
    flag_unpack = struct.Struct(flag_fmt).unpack_from

    with open(filename, 'rb') as f:
        header = head_unpack(f.read(head_len))
        num_players = header[0]
        num_rounds = header[1]
        player_no_fmt = f'={num_players}H'
        player_no_len = struct.calcsize(player_no_fmt)
        f.read(player_no_len)
        flags = flag_unpack(f.read(flag_len))

    return num_players, num_rounds, flags
