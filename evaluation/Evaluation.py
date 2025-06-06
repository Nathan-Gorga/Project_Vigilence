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
from numpy import arange

from extraction.Extraction import extractChannelsFromXdf
from detection.Detection import detectChannelsEOGEvents



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
        raise ValueError(f"Valeur de vérité inconnue: {expected_outcome}")


    test_data["outcome"] = {
        "blinks_found": num_events,
        "result": "PASS" if test_passed else "FAIL"
    }

    with open(json_path, "w") as f:
        json.dump(test_data, f, indent=4)

    if not test_passed:
        print(f"❌ Test échoué pour {filepath}")
        print(f"   Attendu : {expected_blinks} blinks, Détecté : {num_events}")
    else:
        print(f"✅ Test réussi pour {filepath}")

    return test_passed


def batchTest(json_folder: str):
    """
    Lance tous les tests dans le dossier json_folder
    """
    folder = Path(json_folder)
    json_files = list(folder.glob("*.json"))

    successes = 0
    failures = 0

    for json_file in json_files:
        if oneTest(str(json_file)):
            successes += 1
        else:
            failures += 1

    print(f"\nRésultat global : {successes} succès, {failures} échecs sur {len(json_files)} tests")


