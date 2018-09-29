import struct
from pathlib import Path
from typing import List, Tuple, Union


def read_chunks(f, length):
    while True:
        data = f.read(length)
        if not data:
            break
        yield data


def read_lte(filename: Union[str, Path]) -> List[Tuple[str, str, float]]:
    with open(filename, "rb") as f:
        while True:
            player_data = f.read(36+6+25)
            if not player_data:
                break
            name = player_data[:36]
            rating = float(player_data[36:42])
            town = player_data[42:]
            print(name, rating, town)


def read_re(filename: Union[str, Path]) -> List[Tuple[int, int, int, int, int]]:
    struct_fmt = '=bBHHH'
    struct_len = struct.calcsize(struct_fmt)
    struct_unpack = struct.Struct(struct_fmt).unpack_from

    with open(filename, "rb") as f:
        results = [struct_unpack(chunk) for chunk in read_chunks(f, struct_len)]

    return results


def read_tin(filename: Union[str, Path]) -> Tuple[int, int, Tuple[int, int]]:
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

filename = '/home/adam/Downloads/Poznan_2018_export/poznan.re'
# filename = '/home/adam/Downloads/test.re'
filename_tin = '/home/adam/Downloads/test.tin'
res = read_re(filename)
print(res)
res2 = read_tin(filename_tin)
print(res2)
filename_lte = '/home/adam/Downloads/Poznan_2018_export/poznan.lte'
res3 = read_lte(filename_lte)



res = read_tin('/home/adam/Downloads/Poznan_2018_export/poznan.tin')
print(res)