####################################
#        RULLES OF PRODUCTION      #
#  1. MODULARITY!!!                #
#  2. ABC : Always Be Committing   #
#  3. 1 feature = 1 branch         #
#  4. use type annotation          #
#  5. plan before coding    	   #
#  6. unit tests for all functions #
####################################

from Extraction.Extraction import extractChannelsFromXdf

if __name__ == "__main__":
    filepath :str = r'data\one_blink_nathan.xdf'
    selected_channels: list[int] = [1,2]
    
    channels: list[list[float]] = extractChannelsFromXdf(filepath,selected_channels)
    
    print(channels[0])