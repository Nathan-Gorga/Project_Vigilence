####################################
#        RULLES OF PRODUCTION      #
#  1. MODULARITY!!!                #
#  2. ABC : Always Be Committing   #
#  3. 1 feature = 1 branch         #
#  4. use type annotation          #
#  5. plan before coding    	   #
#  6. unit tests for all functions #
####################################

from extraction.Extraction import extractChannelsFromXdf
from visualize.Visualize import printData
from numpy import arange

if __name__ == "__main__":
    filepath :str = r'data\one_blink_nathan.xdf'
    selected_channels: list[int] = [1,3]
    
    [ channels, sfreq ] = extractChannelsFromXdf(filepath,selected_channels)
    
    print(sfreq)
    
    chosen_channels = arange(0,len(selected_channels))
    
    #visualize
    printData(channels,chosen_channels)