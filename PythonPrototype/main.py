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
from detection.Detection import detectWithPattern, removeDoubles
from evaluation.Evaluation import batchTest, getTestData
from pattern.Pattern import createPattern
from include import BASICALLY_ZERO

if __name__ == "__main__":
    
    filepath :str = r'data\sub-nathan_ses-S001_task-clean_blink_calibration_run-001_eeg.xdf'
    selected_channels: list[int] = [1,3]

    [ channels, sfreq ] = extractChannelsFromXdf(filepath,selected_channels, extract_sfreq=True)
    
    patternChannel1, patternChannel2 = createPattern()
    
    ret1 = detectWithPattern(patternChannel1,channels[0])
    ret2 = detectWithPattern(patternChannel2,channels[1])

    eog1 = removeDoubles(ret1['normal_blink'])
    eog2 = removeDoubles(ret2['normal_blink'])
    
    
    printData(channels,[0,1], viewType="detected_eogs", eog_events=[eog1,eog2])
    
    
    # printData(channels,[0,1], viewType="threshold", thresh=[BASICALLY_ZERO,-BASICALLY_ZERO])
    

    # chosen_channels = arange(0,len(selected_channels))
        
    # eog_events = detectChannelsEOGEvents(channels,sfreq)

    # printData(channels, chosen_channels, viewType="detected_eogs",eog_events=eog_events)
    
    
    
    
    
    