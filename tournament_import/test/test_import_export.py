from pathlib import Path
from filecmp import cmp

from tournament import Tournament
from tempfile import TemporaryDirectory


def test_sm_import_and_export():
    test_sm_export_filepath = Path(__file__).parent / 'poznan/poznan.re'
    tour = Tournament('Poznań 2018', 'GW', 'Poznań')
    tour.read_from_scrabble_manager(test_sm_export_filepath)
    with TemporaryDirectory() as tmpdir:
        tour.export_t(Path(tmpdir) / 'test_a.t')
        new_tour = Tournament('Poznań 2018', 'GW', 'Poznań')
        new_tour.read_from_t(Path(tmpdir) / 'test_a.t')
        new_tour.export_re(Path(tmpdir) / 'test_re.re')
        assert cmp(test_sm_export_filepath, Path(tmpdir) / 'test_re.re')
