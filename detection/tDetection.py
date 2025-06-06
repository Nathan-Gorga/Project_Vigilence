import pytest
from Detection import detectEOGEvents

@pytest.fixture
def dummy_signal():
    # Un signal factice avec des "blinks" visibles
    sfreq = 250  # Hz
    import numpy as np
    duration = 5  # 2 sec
    n_samples = sfreq * duration
    signal = [0.0] * n_samples
    # Ajout de 3 blinks simulés
    signal[100] = 5.0
    signal[500] = 6.0
    signal[900] = 7.0
    return [signal], sfreq

def test_detect_eog_event_runs(dummy_signal):
    signal, sfreq = dummy_signal
    result = detectEOGEvents(signal, sfreq)
    
    # Test que la fonction retourne une liste
    assert isinstance(result, list)

    # Test que tous les éléments sont des entiers
    assert all(isinstance(x, int) for x in result)

