# -*- coding: utf-8 -*-

import numpy as np
import pylab as plt
from matplotlib import animation, lines

NCOUNT = 7

class Parent() :

    def __init__(self, xcenter, ycenter, speed, ax, top, color=None) :
        self.xcenter = xcenter
        self.ycenter = ycenter
        self.top = top

        self.speed = speed
        self.ax = ax
        self.color = color or "red"
        self.xvalues, self.yvalues = self.positions()

        self.circle = plt.Circle((xcenter, ycenter), 0.5, fc='white', axes=self.ax)
        self.cline, = ax.plot(self.xvalues, self.yvalues, color=color)
        self.pline, = self.ax.plot([], [], "--", color="#696969")
        
    def positions(self) :
        values = np.arange(0, 360)
        xvalues = self.xcenter + 3 * np.sin(np.radians(values * self.speed))
        yvalues = self.ycenter + 3 * np.cos(np.radians(values * self.speed))
        return xvalues, yvalues

    def init_animate(self) :
        self.circle.center = (self.xcenter, self.ycenter)
        self.ax.add_patch(self.circle)
        return self.pline, self.circle

    def get_xvalue(self, i) :
        speed = NCOUNT
        center = self.xcenter + 10 * (NCOUNT - 1)
        return center + 3 * np.sin(np.radians(i * speed))

    def get_yvalue(self, i) :
        speed = NCOUNT
        center = self.ycenter - 10 * (NCOUNT - 1)
        return center + 3 * np.cos(np.radians(i * speed))

    def animate(self, i) :
        self.circle.center = (self.xvalues[i], self.yvalues[i])

        if self.top :
            self.pline.set_xdata((self.xvalues[i], self.xvalues[i]))
            self.pline.set_ydata((self.yvalues[i], self.get_yvalue(i)))
           
        else :
            self.pline.set_xdata((self.xvalues[i], self.get_xvalue(i)))
            self.pline.set_ydata((self.yvalues[i], self.yvalues[i]))
            
        return self.pline, self.circle

class Hybrid() :

    def __init__(self, xcenter, ycenter, xspeed, yspeed, ax, color=None) :
        self.xcenter = xcenter
        self.ycenter = ycenter

        self.xspeed = xspeed
        self.yspeed = yspeed
        
        self.ax = ax
        self.color = color or "red"
        self.xvalues, self.yvalues = self.positions()

        self.circle = plt.Circle((xcenter, ycenter), 0.5, fc='white', axes=self.ax)
        self.cline, = ax.plot(self.xvalues, self.yvalues, color=color)

    def positions(self) :
        values = np.arange(0, 360)
        xvalues = self.xcenter + 3 * np.sin(np.radians(values * self.xspeed))
        yvalues = self.ycenter + 3 * np.cos(np.radians(values * self.yspeed))
        return xvalues, yvalues

    def init_animate(self) :
        self.circle.center = (self.xcenter, self.ycenter)
        self.ax.add_patch(self.circle)
        return self.cline, self.circle

    def animate(self, i) :
        self.circle.center = (self.xvalues[i], self.yvalues[i])
        self.cline.set_data(self.xvalues[:i], self.yvalues[:i])
        return self.cline, self.circle

def mix_color(c1, c2) :
    return [((c1[idx] + c2[idx]) / 510) for idx in range(3)]

def run() :
    
    animations = []
    fig, ax = plt.subplots(1, 1, figsize=(6,6))

    colors = [(171,61,67), (207, 155, 100), (238, 237, 170),
    (131, 205, 147), (135, 214, 226), (168, 106, 139), (79, 60, 102)]

    ax.set_xlim(0, 10 * (NCOUNT + 1))
    ax.set_ylim(0, 10 * (NCOUNT + 1))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor('#343134')

    for i in range(1, NCOUNT + 1) :
        for j in range(1, NCOUNT + 1) :

            if i == j == 1 : continue

            xposition = i * 10
            yposition = ((NCOUNT + 1) * 10) - (j * 10)
            color = mix_color(colors[i-1], colors[j-1])

            if i == 1 or j == 1 : 
                speed = max((i, j))

                top = i != 1
                aa = Parent(xposition, yposition, speed, ax, top, color=color)

            else :
                aa = Hybrid(xposition, yposition, i, j, ax, color=color)

            animations.append(aa)

    init_fun = lambda : [patch for aa in animations for patch in aa.init_animate()]
    anim_fun = lambda i : [patch for aa in animations for patch in aa.animate(i)]

    anim = animation.FuncAnimation(fig, 
                               func      = anim_fun, 
                               init_func = init_fun, 
                               frames    = 360, 
                               interval  = 30,
                               blit      = True)

    plt.show()

if __name__ == "__main__" :
    run()