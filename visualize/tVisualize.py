import pytest
from unittest.mock import patch, MagicMock
from Visualize import printChannels, printData 


def sample_channels(n_channels=3, length=10):
    return [[float(i + j) for j in range(length)] for i in range(n_channels)]


def test_print_channels_single_channel(monkeypatch):
    channels = sample_channels(1)

    with patch("matplotlib.pyplot.subplots") as mock_subplots:
        fig = MagicMock()
        ax = MagicMock()
        mock_subplots.return_value = (fig, ax)
        
        printChannels(channels)

        mock_subplots.assert_called_once_with(1, 1, figsize=(10, 3), sharex=True)
        assert ax.plot.called
        assert ax.scatter.called
        assert ax.set_ylabel.called
        assert ax.set_xlabel.called or ax.set_xlabel.call_count == 0


def test_print_channels_multiple(monkeypatch):
    channels = sample_channels(4)

    with patch("matplotlib.pyplot.subplots") as mock_subplots:
        fig = MagicMock()
        axs = [MagicMock() for _ in range(4)]
        mock_subplots.return_value = (fig, axs)

        printChannels(channels)

        assert mock_subplots.call_count == 1
        for ax in axs:
            assert ax.plot.called
            assert ax.scatter.called
            assert ax.set_ylabel.called
        axs[-1].set_xlabel.assert_called_once_with("Sample Index")


def test_print_data_channelOnly(monkeypatch):
    channels = sample_channels(3)

    with patch("matplotlib.pyplot.subplots") as mock_subplots, \
         patch("matplotlib.pyplot.tight_layout") as mock_layout, \
         patch("matplotlib.pyplot.show") as mock_show:
        
        fig = MagicMock()
        axs = [MagicMock() for _ in range(2)]
        mock_subplots.return_value = (fig, axs)

        printData(channels, [0, 2], viewType="channelOnly")

        mock_layout.assert_called_once()
        mock_show.assert_called_once()
        assert axs[0].plot.called


def test_print_data_invalid_index():
    channels = sample_channels(2)
    with pytest.raises(IndexError):
        printData(channels, [5], viewType="channelOnly")
