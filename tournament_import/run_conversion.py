from pathlib import Path

from tournament import Tournament
from reader import read_re, read_lte


tour = Tournament('Mistrzostwa TSH', 'Adam Kłimónt', 'Cambridge')
tour.read_from_t('/home/adam/code/tsh/samplepl/a.t')
tour.export_re('/home/adam/Downloads/test.re')
tour.export_tin('/home/adam/Downloads/test.tin')
tour.export_lte('/home/adam/Downloads/test.lte')
tour.export_nag('/home/adam/Downloads/test.nag')
tour.export_smt('/home/adam/Downloads/test.smt')
# games = tour.get_players_games(8)

# print(games)
# # for g in tour.games:
# #     print(g)
# for p in tour.players:
#     print(p)

newtour = Tournament('Poznań', 'Grzegorz', 'Poznań')
newtour.read_from_scrabble_manager('/home/adam/Downloads/turnieje/Documents/kolobrzeg/kolobrzeg.re')

for r in range(9, 12):
    newtour.export_t(f'/home/adam/code/tsh/samplekolobrzeg/a.t_{r}', last_round=r)

newtour = Tournament('Poznań', 'Grzegorz', 'Poznań')
newtour.read_from_scrabble_manager('/home/adam/Downloads/turnieje/Documents/jaworzno/jaworzno.re')
for r in range(9, 12):
    newtour.export_t(f'/home/adam/code/tsh/samplekonojady2018/a.t_{r}', last_round=r)

newtour = Tournament('Poznań', 'Grzegorz', 'Poznań')
newtour.read_from_scrabble_manager('/home/adam/Downloads/turnieje/Poznan_2018_export/poznan.re')
for r in range(10, 13):
    newtour.export_t(f'/home/adam/code/tsh/samplepoznan18/a.t_{r}', last_round=r)


newtour = Tournament('LeMans', 'Grzegorz', 'Poznań')
newtour.read_from_scrabble_manager('/home/adam/Downloads/turnieje/mp_lemans/lemans2017/lemans.re')
for r in range(17, 24):
    newtour.export_t(f'/home/adam/code/tsh/samplelemans17/a.t_{r}', last_round=r)

newtour = Tournament('MP17', 'Grzegorz', 'Poznań')
newtour.read_from_scrabble_manager('/home/adam/Downloads/turnieje/mp_lemans/mp2017/mp.re')
for r in range(11, 15):
    newtour.export_t(f'/home/adam/code/tsh/samplemp17/a.t_{r}', last_round=r)

newtour = Tournament('PP18', 'Grzegorz Wiączkowski', 'Legnica')
newtour.read_from_scrabble_manager('/home/adam/Downloads/turnieje/pp18/pp.re')
newtour.export_t(f'/home/adam/code/tsh/pp2018/allplayers.t_test', last_round=0)

newtour = Tournament('Wałcz 2005', 'Grzegorz Wiączkowski', 'Legnica')
newtour.read_from_scrabble_manager('/home/adam/Downloads/turnieje/walcz_krzyze/walcz2005/walcz.re')
for r in range(8, 12):
    newtour.export_t(f'/home/adam/code/tsh/samplewalcz05/a.t_{r}', last_round=r)

newtour = Tournament('Krzyże 2011', 'Grzegorz Wiączkowski', 'Legnica')
newtour.read_from_scrabble_manager('/home/adam/Downloads/turnieje/walcz_krzyze/krzyze2011/krzyze.re')
for r in range(24, 31):
    newtour.export_t(f'/home/adam/code/tsh/samplekrzyze11/a.t_{r}', last_round=r)

newtour = Tournament('KMP 2018', 'Grzegorz Wiączkowski', 'Legnica')
newtour.read_from_scrabble_manager('/home/adam/Downloads/turnieje/kmp2018/kmp.re')
newtour.export_t(f'/home/adam/code/tsh/samplekmp18/a.t', last_round=30)


pp_path = Path('/home/adam/code/tsh/pp2018')
divs = 'abcdef'
with open(pp_path / 'allplayers.t_test') as f:
    for j, div in enumerate(divs):
        with open(pp_path / f'{div}.t', 'w') as g:
            g.write('')
            for k in range(j*8):
                g.write('Niegrający, Gracz\t0.0; ; off 1; team Niegrający\n')
    div_idx = 0
    snake = 0
    bounce = False
    for i, line in enumerate(f):
        if i < 40:
            if bounce:
                bounce = False
            else:
                div_idx += snake
                if div_idx == 4:
                    bounce = True
                    snake = -1
                elif div_idx == 0:
                    if snake == -1:
                        bounce = True
                    snake = 1

            with open(pp_path / f'{divs[int(div_idx)]}.t', 'a') as g:
                g.write(line)
        else:
            with open(pp_path / f'f.t', 'a') as g:
                g.write(line)

#standings = newtour.calculate_standings(after_round=10)




# filename = '/home/adam/code/tsh/samplepl/a.re'
# # filename = '/home/adam/Downloads/test.re'
# filename = '/home/adam/Downloads/Poznan_2018_export/poznan.re'
# filename = '/home/adam/Downloads/jaworzno/jaworzno.re'
# res = read_re(filename)
# for i, r in enumerate(res):
#     player = i // 13 + 1
#     runda = (i +1) % 13
#     # if r[0] == 0:
#     print(player, runda, r)
#
# filename = '/home/adam/Downloads/Poznan_2018_export/poznan.lte'
# pl = read_lte(filename)
# for i, p in enumerate(pl):
#     print(i, p)
