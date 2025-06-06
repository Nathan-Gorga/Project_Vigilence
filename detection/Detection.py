from mne.preprocessing.eog import _find_eog_events


def detectEOGEvents(channel_data,sfreq): 
    
    filter_length = f"{len(channel_data)}s" 
    
    temp = channel_data
    eog_events = _find_eog_events(
        eog=temp,
        ch_names=None,
        event_id=998,
        l_freq=1,
        h_freq=10,
        sampling_rate=sfreq,
        first_samp=0,
        filter_length="10s",
        tstart=0,
        thresh=None,
        verbose=False
    )
    return [int(row[0]) for row in eog_events]


def detectChannelsEOGEvents(channels,sfreq):
    ret = []
    
    for channel_data in channels:
        
        ret.append(detectEOGEvents([channel_data],sfreq))
        
    return ret