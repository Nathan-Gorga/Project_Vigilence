import matplotlib.pyplot as plt

def printChannels(channels :list[list[float]]):
    color = ["blue", "green", "red", "purple", "orange", "brown", "pink", "gray"]
    num_channels = len(channels)

    _, axs = plt.subplots(num_channels, 1, figsize=(10, 3 * num_channels), sharex=True)

    # If only 1 channel, axs is not a list
    if num_channels == 1:
        axs = [axs]

    for i, data in enumerate(channels):
        axs[i].plot(range(len(data)), data, color=color[i % len(color)])
        axs[i].set_ylabel(f"Channel {i+1}")
        axs[i].grid(True)

    axs[-1].set_xlabel("Sample Index")



def printData(
    channels :list[list[float]], 
    select_channels, 
    viewType :str="channelOnly", 
    thresh=None
    ):
    send_channels = []
    
    for i in select_channels:
        send_channels.append(channels[i])
        
    match viewType:
        case "channelOnly":
            printChannels(send_channels)
    
    
    plt.tight_layout()
    plt.show()