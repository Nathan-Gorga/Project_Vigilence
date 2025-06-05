from pyxdf import load_xdf
import numpy as np

def extractChannelsFromXdf(filepath:str, selected_channels:list[int]):
    """
    Load an XDF file and extract data for the specified channels.
    
    Parameters:
        filepath (str): Path to the .xdf file
        channels (list or tuple of int): List of 1-based channel indices to extract
    
    Returns:
        dict: keys = channel indices, values = numpy arrays of channel data
    """
    # Load all streams from the file
    streams  = load_xdf(filepath)
    
    # Dictionary to store extracted channel data
    extracted_data = []
    
    for ch in selected_channels:
        # Adjust for 0-based Python indexing
        stream_index = ch - 1
        
        if stream_index < 0 or stream_index >= len(streams):
            raise IndexError(f"Channel index {ch} out of range. File contains {len(streams)} streams.")
        
        stream = streams[stream_index]
        
        # Get the time_series data for this stream (should be numpy array or list of lists)
        data = np.array(stream['time_series'])
        
        extracted_data.append(data)
    
    return extracted_data
