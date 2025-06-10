import pytest
from unittest.mock import patch

# Assuming your function is defined in extraction.py

# Simulated XDF stream
mock_xdf_data = (
    [{
        'time_series': [
            [1.0, 2.0, 3.0],
            [1.1, 2.1, 3.1],
            [1.2, 2.2, 3.2],
        ],
        'info': {
            'nominal_srate': ['250.0']
        }
    }],
    {}
)


@patch("pyxdf.load_xdf", return_value=mock_xdf_data)
def test_extract_single_channel(mock_load):
    from Extraction import extractChannelsFromXdf
    result = extractChannelsFromXdf("dummy.xdf", [0])
    assert result == [
        [1.0, 1.1, 1.2]
    ]


@patch("pyxdf.load_xdf", return_value=mock_xdf_data)
def test_extract_multiple_channels(mock_load):
    from Extraction import extractChannelsFromXdf
    result = extractChannelsFromXdf("dummy.xdf", [0, 2])
    assert result == [
        [1.0, 1.1, 1.2],
        [3.0, 3.1, 3.2]
    ]


@patch("pyxdf.load_xdf", return_value=mock_xdf_data)
def test_extract_with_sampling_rate(mock_load):
    from Extraction import extractChannelsFromXdf
    result = extractChannelsFromXdf("dummy.xdf", [1], extract_sfreq=True)
    assert result[0] == [[2.0, 2.1, 2.2]]
    assert result[1] == 250


@patch("pyxdf.load_xdf", return_value=mock_xdf_data)
def test_invalid_channel_index_high(mock_load):
    from Extraction import extractChannelsFromXdf
    with pytest.raises(IndexError):
        extractChannelsFromXdf("dummy.xdf", [5])


@patch("pyxdf.load_xdf", return_value=mock_xdf_data)
def test_invalid_channel_index_negative(mock_load):
    from Extraction import extractChannelsFromXdf
    with pytest.raises(IndexError):
        extractChannelsFromXdf("dummy.xdf", [-1])



@patch("pyxdf.load_xdf", return_value=mock_xdf_data)
def test_empty_channel_list(mock_load):
    from Extraction import extractChannelsFromXdf
    result = extractChannelsFromXdf("dummy.xdf", [])
    assert result == []
