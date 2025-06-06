import pytest
import matplotlib.pyplot as plt
from unittest.mock import patch
from Visualize import printChannels, printDetectedEOGs, printData  # Replace 'your_module'

# Dummy signal fixture
@pytest.fixture
def dummy_channels():
    return [
        [0.1 * i for i in range(10)], 
        [0.2 * i for i in range(10)]
    ]

@pytest.fixture
def dummy_eog_events():
    return [2, 5, 8]

# Test printChannels runs without error
def test_print_channels_runs(dummy_channels):
    axs = printChannels(dummy_channels)
    assert len(axs) == 2  # We expect 2 subplots for 2 channels

# Test printDetectedEOGs adds lines
def test_print_detected_eogs_runs(dummy_channels, dummy_eog_events):
    axs = printDetectedEOGs(dummy_channels, dummy_eog_events)
    assert len(axs) == 2  # Again, 2 channels means 2 subplots

# Test printData in channelOnly mode
def test_print_data_channel_only(dummy_channels):
    with patch("matplotlib.pyplot.show"):
        printData(dummy_channels, select_channels=[0, 1], viewType="channel_only")

# Test printData in detected_eogs mode
def test_print_data_detected_eogs(dummy_channels, dummy_eog_events):
    with patch("matplotlib.pyplot.show"):
        printData(
            dummy_channels,
            select_channels=[0, 1],
            viewType="detected_eogs",
            eog_events=dummy_eog_events
        )

# Test printData with invalid viewType
def test_print_data_invalid_viewtype(dummy_channels):
    with patch("matplotlib.pyplot.show"):
        with pytest.raises(ValueError):
            printData(dummy_channels, select_channels=[0], viewType="invalid")
