from pyxdf import load_xdf
import numpy as np

def extractChannelsFromXdf(filepath:str, selected_channels:list[int]) -> list[list[float]]:

    dictStreams,_  = load_xdf(filepath)
    stream = dictStreams[0]['time_series']
    
    extracted_data = []

    for ch in selected_channels:
        extracted_data.append(stream[:,ch])
    
    return extracted_data
