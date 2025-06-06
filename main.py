####################################
#        RULLES OF PRODUCTION      #
#  1. MODULARITY!!!                #
#  2. ABC : Always Be Committing   #
#  3. 1 feature = 1 branch         #
#  4. use type annotation          #
#  5. plan before coding    	   #
#  6. unit tests for all functions #
#  7. Simple Scales, Fancy Fails   #
####################################

from extraction.Extraction import extractChannelsFromXdf
from visualize.Visualize import printData
from numpy import arange
from detection.Detection import detectChannelsEOGEvents, removeFalsePositives

if __name__ == "__main__":
    filepath :str = r'data\sub-nathan_ses-S001_task-clean_blink_calibration_run-001_eeg.xdf'
    selected_channels: list[int] = [1,3]
    
    [ channels, sfreq ] = extractChannelsFromXdf(filepath,selected_channels, extract_sfreq=True)
    
    chosen_channels = arange(0,len(selected_channels))
        
    eog_events = detectChannelsEOGEvents(channels,sfreq)
    
    printData(channels, chosen_channels, viewType="detected_eogs",eog_events=eog_events)