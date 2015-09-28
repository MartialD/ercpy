import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from skimage import draw
# import matplotlib.cm as cm

def fib(n):    # write Fibonacci series up to n
    a, b = 0, 1
    while b < n:
        print b,
        a, b = b, a+b

def fib2(n): # return Fibonacci series up to n
    result = []
    a, b = 0, 1
    while b < n:
        result.append(b)
        a, b = b, a+b
    return result

class RoiRect(object):
    ''' Class for getting a mouse drawn rectangle
    Based on the example from:
    http://matplotlib.org/users/event_handling.html#draggable-rectangle-exercise
    Note that:
    
    * It makes only one roi
    
    '''
    def __init__(self):
        self.ax = plt.gca()
        self.rect = Rectangle((0,0), 1, 1,fc='none', ec='r')
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.ax.add_patch(self.rect)
        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        print 'press'
        self.x0 = event.xdata
        self.y0 = event.ydata
        self.rect.set_linestyle('dashed')
        self.set = False

    def on_release(self, event):
        print 'release'
        self.x1 = event.xdata
        self.y1 = event.ydata
        self.rect.set_width(self.x1 - self.x0)
        self.rect.set_height(self.y1 - self.y0)
        self.rect.set_xy((self.x0, self.y0))
        self.rect.set_linestyle('solid')
        self.ax.figure.canvas.draw()
        self.set = True
        self.ax.figure.canvas.mpl_disconnect(self.on_press)
        self.ax.figure.canvas.mpl_disconnect(self.on_release)
        self.ax.figure.canvas.mpl_disconnect(self.on_motion)
        
    def on_motion(self, event):
        # on motion will move the rect if the mouse
        if self.x0 is None: return
        if self.set: return
        # if event.inaxes != self.rect.axes: return
        self.x1 = event.xdata
        self.y1 = event.ydata
        self.rect.set_width(self.x1 - self.x0)
        self.rect.set_height(self.y1 - self.y0)
        self.rect.set_xy((self.x0, self.y0))
        self.ax.figure.canvas.draw()

class RoiPoint(object):
    ''' Class for getting a mouse drawn rectangle
    Based on the example from:
    http://matplotlib.org/users/event_handling.html#draggable-rectangle-exercise
    Note that:
    
    * It makes only one roi
    
    '''
    def __init__(self):
        self.ax = plt.gca()
#        self.rect = Rectangle((0,0), 1, 1,fc='none', ec='r')
        self.x0 = None
        self.y0 = None
        self.visible = True
        self.set = False
        self.plt_style = 'r+'
#        self.x1 = None
#        self.y1 = None
#        self.ax.add_patch(self.rect)
        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
#        self.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if not self.set:        
            print 'press'
            self.x0 = event.xdata
            self.y0 = event.ydata
        
            self.draw()

    def on_release(self, event):
        if not self.set:
            print 'release'
#        self.x1 = event.xdata
#        self.y1 = event.ydata
#        self.rect.set_width(self.x1 - self.x0)
#        self.rect.set_height(self.y1 - self.y0)
#        self.rect.set_xy((self.x0, self.y0))
#        self.rect.set_linestyle('solid')
            self.ax.figure.canvas.draw()
            self.set = True
            self.ax.figure.canvas.mpl_disconnect('button_press_event')
            self.ax.figure.canvas.mpl_disconnect('button_release_event')

    def draw(self):
        if not self.visible:
            return
        self.ax.plot(self.x0, self.y0, self.plt_style)
        
#    def on_motion(self, event):
#        # on motion will move the rect if the mouse
#        if self.x0 is None: return
#        if self.set: return
#        # if event.inaxes != self.rect.axes: return
#        self.x1 = event.xdata
#        self.y1 = event.ydata
#        self.rect.set_width(self.x1 - self.x0)
#        self.rect.set_height(self.y1 - self.y0)
#        self.rect.set_xy((self.x0, self.y0))
#        self.ax.figure.canvas.draw()
#class roi_rect_new(object):
#    ''' Class for getting a mouse drawn rectangle
#    '''
#    def __init__(self):
#        self.ax = plt.gca()
#        self.rect = Rectangle((0,0), 1, 1, facecolor='None', edgecolor='green')
#        self.x0 = None
#        self.y0 = None
#        self.x1 = None
#        self.y1 = None
#        self.ax.add_patch(self.rect)
#        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_press)
#        self.ax.figure.canvas.mpl_connect('button_release_event', self.on_release)
#        self.ax.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)
#    def on_press(self, event):
#        print 'press'
#        self.x0 = event.xdata
#        self.y0 = event.ydata    
#        self.x1 = event.xdata
#        self.y1 = event.ydata
#        self.rect.set_width(self.x1 - self.x0)
#        self.rect.set_height(self.y1 - self.y0)
#        self.rect.set_xy((self.x0, self.y0))
#        self.rect.set_linestyle('dashed')
#        self.ax.figure.canvas.draw()
#    def on_motion(self,event):
#        if self.on_press is True:
#            return
#        self.x1 = event.xdata
#        self.y1 = event.ydata
#        self.rect.set_width(self.x1 - self.x0)
#        self.rect.set_height(self.y1 - self.y0)
#        self.rect.set_xy((self.x0, self.y0))
#        self.rect.set_linestyle('dashed')
#        self.ax.figure.canvas.draw()
#    def on_release(self, event):
#        print 'release'
#        self.x1 = event.xdata
#        self.y1 = event.ydata
#        self.rect.set_width(self.x1 - self.x0)
#        self.rect.set_height(self.y1 - self.y0)
#        self.rect.set_xy((self.x0, self.y0))
#        self.rect.set_linestyle('solid')
#        self.ax.figure.canvas.draw()
#        print self.x0,self.x1,self.y0,self.y1
#        return [self.x0,self.x1,self.y0,self.y1]
        
def poly_to_mask(vertex_row_coords, vertex_col_coords, shape):
    '''
    Creates a poligon mask
    '''
    fill_row_coords, fill_col_coords = draw.polygon(vertex_row_coords, vertex_col_coords, shape)
    mask = np.zeros(shape, dtype=np.bool)
    mask[fill_row_coords, fill_col_coords] = True
    return mask

def wrap_to_pi(angle):
    """
    Wrap a given angle in radians to the range -pi to pi.
    
    @param angle : The angle to be wrapped
    @param type angle : float
    @return : Wrapped angle
    @rtype : float
    """
    return np.mod(angle+np.pi,2.0*np.pi)-np.pi
    
def wrap(angle):
    '''
    Wrap a given angle in radians to the range 0 to 2pi.
    
    @param angle : The angle to be wrapped
    @param type angle : float
    @return : Wrapped angle
    @rtype : float
    '''
    return angle % (2 * np.pi )