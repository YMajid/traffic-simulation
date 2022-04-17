from model import NSModel
import matplotlib.pyplot as plt
from matplotlib import colors, animation
import matplotlib
import os
import matplotlib.patches as mpatches
from zipper import Zipper

def animate_ns():
    if os.name == 'nt':
        plt.rcParams['animation.ffmpeg_path'] = 'C:\\ffmpeg\\bin\\ffmpeg.exe'

    all_data = []
    model = NSModel(prob=0.3,
                    n_lanes=10,
                    lane_len=200,
                    max_velocity=5,
                    lane_density=0.3,
                    lane_changes=True,
                    initialize_highway=True)

    all_data.append(model.highway)
    for _ in range(200):
        model.simulate()
        all_data.append(model.highway)

    fig = plt.figure(figsize=(30, 2))
    bounds = [-2, -0.1, 10]
    cmap = colors.ListedColormap(['white', 'red'])
    norm = colors.BoundaryNorm(bounds, cmap.N)

    im = plt.imshow(model.highway, interpolation=None,
                    cmap=cmap, norm=norm)
    im.axes.get_xaxis().set_ticks([])
    im.axes.get_yaxis().set_ticks([])
    plt.title("Bird's eye view of 10 lane highway (NS Model)")
    plt.xlabel('Position')
    plt.ylabel('Lanes')
    def animate_func(i):
        z = i//6
        im.set_array(all_data[z])
        return [im]
    
    
    labels = ['Empty space on highway', 'Car with P=0.3, Density=0.3']
    patches = [ mpatches.Patch(color=['white', 'red'][i], label=labels[i]) for i in range(2) ]
    plt.legend(handles=patches, bbox_to_anchor=(0, 0), loc=2, borderaxespad=0. )
    ani = animation.FuncAnimation(
        fig, animate_func, frames=len(all_data) * 6, interval=1)
    writervideo = matplotlib.animation.FFMpegWriter(fps=24)

    ani.save('./ns.mp4', writer=writervideo)

def animate_zipper():
    if os.name == 'nt':
        plt.rcParams['animation.ffmpeg_path'] = 'C:\\ffmpeg\\bin\\ffmpeg.exe'

    all_data = []

    model =  Zipper(prob=0.3,
                        n_lanes=10,
                        lane_len=200,
                        max_velocity=5,
                        lane_density=0.3,
                        lane_changes=True,
                        n_blocked= 5,
                        portion_blocked=0.2)
        
    all_data.append(model.highway)
    for _ in range(200):
        model.simulate()
        all_data.append(model.highway)
    fig = plt.figure(figsize=(30, 2))
    bounds = [-4,-1.99, -0.1, 10]
    cmap = colors.ListedColormap(['black','white', 'red'])
    norm = colors.BoundaryNorm(bounds, cmap.N)

    im = plt.imshow(model.highway, interpolation=None,
                    cmap=cmap, norm=norm)
    im.axes.get_xaxis().set_ticks([])
    im.axes.get_yaxis().set_ticks([])
    plt.title("Bird's eye view of 10 lane highway (Zipper Model)")
    plt.xlabel('Position')
    plt.ylabel('Lanes')
    def animate_func(i):
        z = i//6
        im.set_array(all_data[z])
        return [im]
    
    
    labels = ['Blocked space on highway','Empty space on highway', 'Car with P=0.3, Density=0.3']
    patches = [ mpatches.Patch(color=['black','white', 'red'][i], label=labels[i]) for i in range(3) ]
    plt.legend(handles=patches, bbox_to_anchor=(-0.15, 0.5), loc=2, borderaxespad=0. )
    ani = animation.FuncAnimation(
        fig, animate_func, frames=len(all_data) * 6, interval=1)
    writervideo = matplotlib.animation.FFMpegWriter(fps=24)

    ani.save('./zipper.mp4', writer=writervideo)
    
if __name__ == "__main__":
    animate_ns()
    animate_zipper()
