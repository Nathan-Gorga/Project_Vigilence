from pyxdf import load_xdf

def extractChannelsFromXdf(filepath:str, selected_channels:list[int]) -> list[list[float]]:

    try :
        dictStreams,_  = load_xdf(filepath)
    except Exception:
        raise FileNotFoundError(f"file : {filepath} does not exist")
    
    print(dictStreams)
    
    stream = dictStreams[0]['time_series']
    
    extracted_data = []

    size = len(stream)
    for ch in selected_channels:
        
        if ch < 0 or ch >= size : raise IndexError(f"stream only has {size} channels, index was {ch}")
        extracted_data.append([row[ch] for row in stream])
    
    return extracted_data
