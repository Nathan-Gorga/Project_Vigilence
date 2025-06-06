

# Actual logic to test
from ..detection.Detection import removeFalsePositives
# ---------- Unit Tests ----------

def test_all_events_match_within_tolerance():
    input_data = [[100, 200, 300], [104, 195, 296]]  # within ±BLINK_TIME
    expected = [[100, 200, 300], [104, 195, 296]]
    assert removeFalsePositives(input_data) == expected

def test_some_events_out_of_tolerance():
    input_data = [[100, 200, 400], [100, 280, 400]]  # 280 not within ±BLINK_TIME of 200
    expected = [[100, 400], [100, 400]]
    assert removeFalsePositives(input_data) == expected

def test_no_events_within_tolerance():
    input_data = [[100, 200], [300, 400]]
    expected = [[], []]
    assert removeFalsePositives(input_data) == expected

def test_one_channel_empty():
    input_data = [[100, 200], []]
    expected = [[], []]
    assert removeFalsePositives(input_data) == expected

def test_both_channels_empty():
    input_data = [[], []]
    expected = [[], []]
    assert removeFalsePositives(input_data) == expected

def test_duplicate_events_still_match():
    input_data = [[100, 200, 200], [204, 100]]  # 204 ≈ 200
    expected = [[100, 200, 200], [204, 100]]
    assert removeFalsePositives(input_data) == expected
