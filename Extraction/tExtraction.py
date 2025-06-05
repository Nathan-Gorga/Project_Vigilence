import pytest
from unittest.mock import patch, MagicMock

# Test Data
mock_time_series = [
    [0.1, 0.2, 0.3],
    [0.4, 0.5, 0.6],
    [0.7, 0.8, 0.9],
]  # 3 samples, 3 channels

# ---- Fixtures and Helpers ----

@pytest.fixture
def mock_xdf(monkeypatch):
    fake_load_xdf = MagicMock(return_value=([
        {'time_series': mock_time_series}
    ], {}))
    monkeypatch.setattr("pyxdf.load_xdf", fake_load_xdf)

# ---- Tests ----

def test_extract_single_channel(mock_xdf):
    from Extraction import extractChannelsFromXdf
    result = extractChannelsFromXdf("fake_path.xdf", [1])
    assert result == [[0.2, 0.5, 0.8]]

def test_extract_multiple_channels(mock_xdf):
    from Extraction import extractChannelsFromXdf
    result = extractChannelsFromXdf("fake_path.xdf", [0, 2])
    assert result == [
        [0.1, 0.4, 0.7],
        [0.3, 0.6, 0.9]
    ]

def test_invalid_channel_index_high(mock_xdf):
    from Extraction import extractChannelsFromXdf
    with pytest.raises(IndexError, match=r"stream only has 3 channels"):
        extractChannelsFromXdf("fake_path.xdf", [3])

def test_invalid_channel_index_negative(mock_xdf):
    from Extraction import extractChannelsFromXdf
    with pytest.raises(IndexError, match=r"index was -1"):
        extractChannelsFromXdf("fake_path.xdf", [-1])

def test_empty_channel_list(mock_xdf):
    from Extraction import extractChannelsFromXdf
    result = extractChannelsFromXdf("fake_path.xdf", [])
    assert result == []

def test_file_load_failure(monkeypatch):
    def fake_load_xdf_fail(*args, **kwargs):
        raise FileNotFoundError("file : nonexistent_file.xdf does not exist")

    monkeypatch.setattr("Extraction.load_xdf", fake_load_xdf_fail)  
    from Extraction import extractChannelsFromXdf
    with pytest.raises(FileNotFoundError):
        extractChannelsFromXdf("nonexistent_file.xdf", [0])