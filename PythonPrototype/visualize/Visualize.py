import matplotlib.pyplot as plt

color = ["blue", "green", "red", "purple", "orange", "brown", "pink", "gray"]


def printChannels(channels :list[list[float]]):
    num_channels = len(channels)

    col = (2 // num_channels)

    _, axs = plt.subplots(num_channels, col, figsize=(10, 3 * num_channels), sharex=True)

    # If only 1 channel, axs is not a list
    if num_channels == 1:
        axs = [axs]


    if col == 1:
        for i, data in enumerate(channels):
            axs[i].plot(range(len(data)), data, color=color[i % len(color)])
            axs[i].scatter(range(len(data)), data, color=color[i % len(color)],s=10)
            axs[i].set_ylabel(f"Channel {i+1}")
            axs[i].grid(True)
    else:
        for c in range(col):
            for i, data in enumerate(channels):
                axs[i][c].plot(range(len(data)), data, color=color[i % len(color)])
                axs[i][c].scatter(range(len(data)), data, color=color[i % len(color)],s=10)
                axs[i][c].set_ylabel(f"Channel {i+1}")
                axs[i][c].grid(True)

    return axs, num_channels, col


def printDetectedEOGs(channels : list[list[float]], eog_events):
    
    assert len(channels) == len(eog_events)
    
    axs, row , col = printChannels(channels)

    sizeChannels = row
    sizeColor = len(color)
    for c in range(col):
        for i in range(sizeChannels):
            sizeEvents = len(eog_events[i])
            for j in range(sizeEvents):
                if col == 1:
                    axs[i].axvline(x=eog_events[i][j], color=color[((i+1)%sizeColor)] , linestyle='--', linewidth=2)
                
                else:
                    axs[i][c].axvline(x=eog_events[i][j], color=color[((i+1)%sizeColor)] , linestyle='--', linewidth=2)
                    
                    
    return axs, row, col
        

def printTest(test_data : list[list[float]],test_eog_events, test_succeed=False):
    #print the channels, 
    axs, row, col = printChannels(test_data)
    
    # print the detected, 
    
    sizeChannels = row
    sizeColor = len(color)
    for c in range(col):
        for i in range(sizeChannels):
            sizeEvents = len(test_eog_events[i])
            for j in range(sizeEvents):
                if col == 1:
                    axs[i].axvline(x=test_eog_events[i][j], color=color[((i+1)%sizeColor)] , linestyle='--', linewidth=2)
                
                else:
                    axs[i][c].axvline(x=test_eog_events[i][j], color=color[((i+1)%sizeColor)] , linestyle='--', linewidth=2)
                   
    return axs, row, col 
    
    
    
def printTreshold(channels :list[list[float]], thresholds : list[list[float]]):

    axs, row , col = printChannels(channels)
    for c in range(col):
        for r in range(row):
            
            if col == 1:
                axs[r].hlines(y = thresholds,xmin=0, xmax=len(channels[0]), linestyle="--")
            else:
                axs[r][c].hlines(y = thresholds,xmin=0, xmax=len(channels[0]), linestyle="--")
            
    return axs, row, col
    


def printData(
    channels :list[list[float]], 
    select_channels, 
    viewType :str="channel_only", 
    thresh=[0],
    eog_events=None
    ):
    
    viewTypes = ["channel_only", "detected_eogs","test_success","test_fail","threshold"]    
    
    if viewType not in viewTypes:
        raise ValueError(f"ViewType : {viewType} does not exist, please choose one from the list : {viewTypes}")
    
    send_channels = []

    for i in select_channels:
        send_channels.append(channels[i])
        
    match viewType:
        case "channel_only":
            _,_,_ = printChannels(send_channels)
        case "detected_eogs":
            _,_,_ = printDetectedEOGs(send_channels,eog_events)
        case "test_success":
            _,_,_ = printTest(channels,eog_events,test_succeed=True)
        case "test_fail":
            _,_,_ = printTest(channels,eog_events,test_succeed=False)
        case "threshold":
            _,_,_ = printTreshold(channels,thresh)
                
        
            
    
    plt.tight_layout()
    plt.show()