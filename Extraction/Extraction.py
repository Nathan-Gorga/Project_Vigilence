from pyxdf import load_xdf


def extractChannelsFromXdf(filepath:str, selected_channels:list[int], extract_sfreq=False):

    try :
        dictStreams,_  = load_xdf(filepath)
    except Exception:
        raise FileNotFoundError(f"file : {filepath} does not exist")
    
    stream = dictStreams[0]['time_series']
    
    if extract_sfreq:
        sfreq = float(dictStreams[0]['info']['nominal_srate'][0])
    
    extracted_data = []

    size = len(stream)
    for ch in selected_channels:
        
        if ch < 0 or ch >= size : raise IndexError(f"stream only has {size} channels, index was {ch}")
        extracted_data.append([row[ch] for row in stream])
    
    if extract_sfreq : return [extracted_data, sfreq]
    return extracted_data
