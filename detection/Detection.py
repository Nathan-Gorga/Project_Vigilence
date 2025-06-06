from mne.preprocessing.eog import _find_eog_events
from include import TOLERANCE
import numpy as np


def isSamePeak(x1,x2):
    return (x1 - TOLERANCE) <= x2 <= (x1 + TOLERANCE)


def eventInChannel(eventA :int, channelB: list[int]):

    for eventB in channelB:

        if isSamePeak(eventA,eventB):        

            return True

    return False


# handles 2 data channels right now, can maybe add a third to make a majority "vote" on the events
def removeFalsePositives(eog_events): 
    
    chA = eog_events[0]
    chB = eog_events[1]
    
    for event in chA.copy():
        
        if not eventInChannel(event, chB):
            chA.remove(event)
    
    
    for event in chB.copy():
        
        if not eventInChannel(event, chA):
            chB.remove(event)
    
    # assert len(chA) == len(chB)
    
    return [chA,chB]
    
    

def detectEOGEvents(channel_data,sfreq):     
    
    TOO_SHORT = 2048
    method = "fir"
    
    signal_length = len(channel_data) 
    if signal_length < TOO_SHORT:
        method = "iir"
    
    eog_events = _find_eog_events(
        eog=channel_data,
        ch_names=None,
        event_id=998,
        l_freq=1,
        h_freq=10,
        sampling_rate=sfreq,
        first_samp=0,
        filter_length="auto",
        tstart=0,
        thresh=None,
        verbose=False,
        filetering_method=method
    )
    return [int(row[0]) for row in eog_events]


def detectChannelsEOGEvents(channels,sfreq):
    ret = []
    
    for channel_data in channels:
        
        ret.append(detectEOGEvents([channel_data],sfreq))
        
    return removeFalsePositives(ret)