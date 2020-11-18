#PLOT MQTT SUB POSITION
import matplotlib.pyplot as plt
import matplotlib.animation as ani
from matplotlib import style

def plot_init(fig,ax1):
        fig = plt.figure()                              #Creates figure obj, following line creates subplot to operate on
        ax1 = fig.add_subplot(111, projection='3d')     #TODO: assign fig and ax1 to vars in start func
        ax1.set_xlabel('X')                             #set axis labels
        ax1.set_ylabel('Y')
        ax1.set_zlabel('Z')

def animate(node_data):                                 #This function is where we can modify all subplots to create a RT graph
                                                        #plots data obtained from nodeinfo_q (may be inefficient, updating when value has not changed)
                                                        #We may have to parse for actual num vals in node_data
        ax1.clear()                                     #Clears out of date graph
        ax1.scatter(node_data[3],node_data[4],node_data[5]) #Plots next location
                                                        #TODO: potentially add additional subplots so we can chart the location of the anchors in the graph

def start(nodeinfo_q):
                                                        #PLOT_INIT Assignments
        plot_init()
        node_info = nodeinfo_q.get()                    #takes the oldest msg in data queue out of the queue
        ani = ani.FuncAnimation(fig, animate, frames = node_info, interval = 250) #creates new thread which calls func animate every 250ms, passing it node_info, modify>
        plt.show()                                      #Creates plot window (Should be called after all other plot code
        while(node_info == "ON"):
                data = nodeinfo_q.get()                 #begins consumer loop
                if(data is "OFF"):
                        break
                else:
                        print(data)

