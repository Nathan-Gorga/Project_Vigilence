from mne.preprocessing.eog import _find_eog_events
import numpy as np

from include import BLINK_DURATION, TOLERANCE
from utils.Utils import isBaseline, isSameEvent, localMaximumIndex
from visualize.Visualize import printData



def mergeEvents(event1 :int, event2 :int, channel :list[int]):
    #create new event
    newEvent = int(np.mean([event1,event2]))

    #store old event index
    leastEvent = event1 if event1 < event2 else event2
    
    print(f"event1 : {event1} | event2 : {event2} | channel : {channel}")
    
    oldIndex = channel.index(leastEvent)
    
    #remove old events
    
    channel.remove(event1)
    channel.remove(event2)
    
    #store new event at old event index
    channel.insert(oldIndex,newEvent)
    
    return channel
    
    

def eventInChannel(eventA :int, channelB: list[int]):

    if len(channelB) == 0: return False
    
    flag = False
    
    previous = -1000 # should not be called the very first time so not a problem
    
    # condition if channelB only has 1 event
    if len(channelB) == 1 and isSameEvent(eventA,previous): return True
    
    temp = channelB.copy()
    
    for eventB in temp:

        if isSameEvent(eventA,eventB):        
        
            if isSameEvent(eventA, previous):
        
                channelB = mergeEvents(previous,eventB,temp)
        
            flag = True
        
        previous = eventB
        
        
    return flag


# handles 2 data channels right now, can maybe add a third to make a majority "vote" on the events
def removeFalsePositives(eog_events): 
    
    chA = eog_events[0]
    chB = eog_events[1]
    
    tempA = chA.copy()
    tempB = chB.copy()
    
    for event in tempA:
        
        if not eventInChannel(event, tempB):
            chA.remove(event)
    
    
    for event in tempB:
        
        if not eventInChannel(event, tempA):
            chB.remove(event)
    
    assert len(chA) == len(chB)
    
    return [chA,chB]
    
    

def detectEOGEvents(channel_data,sfreq):     
    
    
    
    FILTER_LENGTH = 2480
    method = "fir"
    
    signal_length = len(channel_data) 
    
    
    if signal_length < FILTER_LENGTH:
        method = "iir"
    
    eog_events = _find_eog_events(
        eog=[channel_data.copy()],
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

    # adjust detection to local maximum
    finals = []
    
    for row in eog_events:
    
        bMin = max(row[0] - TOLERANCE, 0)
        bMax = min(row[0] + TOLERANCE, signal_length - 1)

        buffer = list(channel_data[bMin : bMax])

        
        index = localMaximumIndex(buffer,bMin)
        
        finals.append(index)

    return finals


def detectChannelsEOGEvents(channels,sfreq):
    ret = []
    
    for channel_data in channels:
        
        ret.append(detectEOGEvents(channel_data,sfreq))
        
    return removeFalsePositives(ret)




def detectWithPattern(pattern :list[float], data : list[float]):
    sizePattern = len(pattern)
    sizeData = len(data)
    
    repeat = sizeData - sizePattern
    ret = {
        "normal_blink" : [],
        "fast_blink" : [],
        "slow_blink" : []        
    }
    
    for i in range(repeat):
        start = i
        end = start + sizePattern
        buffer = np.array(data[start:end])
        if isBaseline(buffer): continue
        
        bMax = max(buffer)
        bMin = min(buffer)
        
        pMax = max(pattern)
        pMin = min(pattern)
        
        bFactor = bMax - bMin
        pFactor = pMax - pMin
        
        scaleFactor = bFactor/pFactor
        
        buffer -= np.array(pattern) * scaleFactor
        
        if isBaseline(buffer):
            print(f"Found normal blink at {i}") 
            ret["normal_blink"].append(i) 
            # printData([list(np.array(data)- (([0] * i) + pattern +( [0] * (repeat - i)))),data],[0,1], viewType="threshold", thresh=[BASICALLY_ZERO,-BASICALLY_ZERO])
    return ret
        
def removeDoubles(eog_event): # function could be added to remove false positives
    fin = []
    until = -1
    for event in eog_event:
        if event > until:
            fin.append(event)
            until = event + BLINK_DURATION
    return fin
    