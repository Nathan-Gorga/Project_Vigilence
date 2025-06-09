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
from detection.Detection import detectChannelsEOGEvents
from evaluation.Evaluation import batchTest, getTestData

if __name__ == "__main__":
    filepath :str = r'C:/Users/gorga/CodeProjects/Arduino/Blink/projet_blink/data/saccade_right_nathan.xdf'
    selected_channels: list[int] = [1,3]

    [ channels, sfreq ] = extractChannelsFromXdf(filepath,selected_channels, extract_sfreq=True)

    chosen_channels = arange(0,len(selected_channels))
        
    eog_events = detectChannelsEOGEvents(channels,sfreq)

    printData(channels, chosen_channels, viewType="detected_eogs",eog_events=eog_events)
    
    
    
    
    
    