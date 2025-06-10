# test JSON example :

# {
#     "filepath" : "data/abc.xdf",
#     "expected" : {
#         "outcome" : TRUE_POSITIVE, 
#         "blinks" : 1,
#     },
#     "outcome":{
#         "blinks_found" : 2,
#         "result" : FAIL
#     }
# }
import json
from pathlib import Path
import numpy as np

from extraction.Extraction import extractChannelsFromXdf
from detection.Detection import detectChannelsEOGEvents

def getTestData(json_folder : str):
    folder = Path(json_folder)
    json_files = list(folder.glob("*.json"))    

    ret = []
    for file in json_files:
        with open(str(file)) as f:
            data = json.load(f)
        ret.append(data)
        
    return ret
        

def runTest(filepath :str):
    
    selected_channels: list[int] = [1,3]
    
    [ channels, sfreq ] = extractChannelsFromXdf(filepath,selected_channels, extract_sfreq=True)
    
    return detectChannelsEOGEvents(channels,sfreq)
        


def oneTest(json_path: str) -> bool:
    
    with open(json_path, "r") as f:
        test_data = json.load(f)

    filepath = test_data["filepath"]
    expected_outcome = test_data["expected"]["outcome"]  # "TRUE_POSITIVE" ou "TRUE_NEGATIVE"
    
    expected_blinks = test_data["expected"]["blinks"]

    # Exécution de l'algorithme
    events = runTest(filepath)
    
    num_events = len(events[0])

    # Comparaison avec la vérité terrain
    if expected_outcome == "TRUE_POSITIVE":
        test_passed = expected_blinks == num_events
    elif expected_outcome == "TRUE_NEGATIVE":
        test_passed =  0 == num_events
    else:
        raise ValueError(f"Truth value unknown: {expected_outcome}")


    clean_event = [
        [int(i) for i in events[0]],
        [int(i) for i in events[1]] 
    ]

    test_data["outcome"] = {
        "blinks_found": num_events,
        "result": "PASS" if test_passed else "FAIL",
        "detected" : clean_event
    }

    with open(json_path, "w") as f:
        json.dump(test_data, f, indent=4)

    if not test_passed:
        print(f"❌ Test failed for {filepath}")
        print(f"   Expected : {expected_blinks} blinks, Detected : {num_events}")
    else:
        print(f"✅ Test passed for {filepath}")

    return test_passed


def batchTest(json_folder: str):
    
    folder = Path(json_folder)
    json_files = list(folder.glob("*.json"))

    successes = 0
    failures = 0

    for json_file in json_files:
        if oneTest(str(json_file)):
            successes += 1
        else:
            failures += 1

    print(f"\nSuccess rate : {successes*100/(successes + failures)} % | {successes} successes, {failures} failures for {len(json_files)} tests")


