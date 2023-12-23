from unittest.mock import patch
import pytest
from src.services.temperature.forecast import choose_correct_files


PATH = "data"

@pytest.fixture
def mock_listdir():
    return ['1688497200.wgf4', '1688500800.wgf4', '1688504400.wgf4']


def test_choose_correct_files(mock_listdir):
    from_ts = 1688497200
    to_ts = 1688504400

    with patch('os.listdir', return_value=mock_listdir):
        result = choose_correct_files(PATH, from_ts, to_ts)

    assert result == ['1688497200.wgf4', '1688500800.wgf4', '1688504400.wgf4']

def test_choose_correct_files_empty_list(mock_listdir):
    from_ts = 1689504400
    to_ts = 1698504400

    with patch('os.listdir', return_value=mock_listdir):
        result = choose_correct_files(PATH, from_ts, to_ts)

    assert result == []

