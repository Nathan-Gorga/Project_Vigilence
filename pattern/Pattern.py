from extraction.Extraction import extractChannelsFromXdf
import numpy as np
from visualize.Visualize import printData
from detection.Detection import detectChannelsEOGEvents
from include import BLINK_DURATION, TOLERANCE


def avgEvents(events : list[float]) -> list[float]:
    
    if events == []: return []
    
    sizeEventList = len(events)
    
    if sizeEventList == 1: return events
    
    template = np.array(events[0])
    
    for event in events[1:]:
        template += np.array(event)
        
    template /= sizeEventList

    return list(template)


def createPattern(type="blink"):
    blink_file = r'data\sub-nathan_ses-S001_task-clean_blink_calibration_run-001_eeg.xdf'
    selected_channels = [1,3]
    match(type):
        case "blink":
            data, sfreq = extractChannelsFromXdf(blink_file,selected_channels,extract_sfreq=True)
            
    # chosen_channels = np.arange(0,len(selected_channels))

    
    eog_events = detectChannelsEOGEvents(data,sfreq)


    
    events = []
    
    sizeChannel = len(eog_events)
    
    sizeData = len(data[0])
    
    
    
    for channel in range(sizeChannel):
        ch = []
        for eog in eog_events[channel]:
            start = eog - TOLERANCE
            end = min(start + BLINK_DURATION,sizeData-1)
            
            ch.append(data[channel][start:end])
        events.append(ch)
            
            
    
    firstPattern = avgEvents(events[0])
    secondPattern = avgEvents(events[1])
    
    return firstPattern, secondPattern
    