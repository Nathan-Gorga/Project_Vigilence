from mne.preprocessing.eog import _find_eog_events


def detectEOGEvent(channel_data,sfreq): 
    
    filter_length = f"{len(channel_data)*3}s" 
    
    eog_events = _find_eog_events(
        eog=channel_data,
        ch_names=None,
        event_id=998,
        l_freq=1,
        h_freq=10,
        sampling_rate=sfreq,
        first_samp=0,
        filter_length=filter_length,
        tstart=0,
        thresh=None,
        verbose=False
    )
    return [int(row[0]) for row in eog_events]
