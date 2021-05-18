import numpy as np
import math

try :
    from . import my_solid_python_basic_shape as msp
except :
    import my_solid_python_basic_shape as msp


class regular_polygon(msp.polygon):
    def __init__(self, N, radius, alignToX = True):
        
        if(N < 2):
            raise SyntaxError("regular_polygon, must have at least 3 side")
        N+=1
 
        allangles = np.linspace(0, 360 , num=N, endpoint = False )
        if alignToX:
            # try align last bar with the X axis : 
            delta_angle = allangles[1]-allangles[0]
            start_angle = -90 + delta_angle/2
            allangles = [b+start_angle for b in allangles ]
        pts = [[radius*math.cos(math.radians(b)), radius*math.sin(math.radians(b))] for b in allangles ]
        super().__init__(pts)
        self.name = "polygon"
        deltaAngle_degree   = 360.0/N


class hexagon(regular_polygon):
    def __init__(self, radius=None, size=None , alignToX = True):
        if not radius:
            if not size:
                raise SyntaxError("hexagon must have a size defined! ")
            radius = size # for the hexagon Radius = side size ! easy case :)
        super().__init__(N=5,radius=radius, alignToX=alignToX)


class pentagon(regular_polygon):
    def __init__(self, radius=None, size=None, alignToX = True):
        if not radius:
            if not size:
                raise SyntaxError("hexagon must have a size defined! ")
            # via wikipedia:  side_size = 2*R*sin(36degree) ==> 
            radius = size/(2*math.sin(math.radians(36)))
        super().__init__(N=5,radius=radius, alignToX=alignToX)




class junction(msp.polygon)