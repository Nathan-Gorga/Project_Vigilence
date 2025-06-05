from pyxdf import load_xdf
import numpy as np

def extractChannelsFromXdf(filepath:str, selected_channels:list[int]) -> list[list[float]]:

    dictStreams,_  = load_xdf(filepath)
    stream = dictStreams[0]['time_series']
    
    extracted_data = []

    size = len(stream)
    for ch in selected_channels:
        if ch < 0 or ch >= size : raise IndexError(f"stream only has {size} channels, index was {ch}")
        extracted_data.append(stream[:,ch])
    
    return extracted_data
