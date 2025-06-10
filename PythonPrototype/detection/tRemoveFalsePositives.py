import pytest
from .Detection import removeFalsePositives

TOLERANCE = 150 / 6

def test_basic_match():
    eog_events = [
        [100, 300],
        [102, 299]
    ]
    result = removeFalsePositives([eog_events[0][:], eog_events[1][:]])
    assert result == [[100, 300], [102, 299]]

def test_no_match():
    eog_events = [
        [100, 300],
        [200, 400]
    ]
    result = removeFalsePositives([eog_events[0][:], eog_events[1][:]])
    assert result == [[], []]

def test_partial_match():
    eog_events = [
        [100, 300, 500],
        [99, 450]
    ]
    result = removeFalsePositives([eog_events[0][:], eog_events[1][:]])
    assert result == [[100], [99]]

def test_all_match_with_tolerance():
    eog_events = [
        [100, 200, 300],
        [120, 180, 299]
    ]
    result = removeFalsePositives([eog_events[0][:], eog_events[1][:]])
    # All within TOLERANCE (25), but some merging may have occurred
    assert len(result[0]) == len(result[1]) == 3

def test_empty_input():
    eog_events = [
        [],
        []
    ]
    result = removeFalsePositives([eog_events[0][:], eog_events[1][:]])
    assert result == [[], []]

def test_one_empty():
    eog_events = [
        [100, 200],
        []
    ]
    result = removeFalsePositives([eog_events[0][:], eog_events[1][:]])
    assert result == [[], []]

def test_close_but_not_within_tolerance():
    eog_events = [
        [100],
        [100 + TOLERANCE + 1]  # Just outside tolerance
    ]
    result = removeFalsePositives([eog_events[0][:], eog_events[1][:]])
    assert result == [[], []]

def test_merging_two_close_events():
    eog_events = [
        [100],
        [90, 110]
    ]
    result = removeFalsePositives([eog_events[0][:], eog_events[1][:]])
    # 90 and 110 should merge to 100, match with 100
    assert result[0] == [100]
    assert result[1] == [100]

def test_duplicate_events_in_one_channel():
    eog_events = [
        [100, 102],
        [101]
    ]
    result = removeFalsePositives([eog_events[0][:], eog_events[1][:]])
    assert result[0] == [101]
    assert result[1] == [101]
