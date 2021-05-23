import numpy as np
import math

try :
    from . import python_to_openscad_basic_shape as msp
except :
    import python_to_openscad_basic_shape as msp


import numpy as np
import math

def rotation_matrix(axis, theta=None):
    """
    Return the rotation matrix associated with counterclockwise rotation about
    the given axis by theta radians.
    #source https://stackoverflow.com/questions/6802577/rotation-of-3d-vector
    """
 
    axis = np.asarray(axis)
    normalised_axis = axis / math.sqrt(np.dot(axis, axis))
    if not theta :
        for b in range(len(normalised_axis)):
            if normalised_axis[b] != 0:
                theta = axis[b]/normalised_axis[b]
        if theta is None :
            raise SyntaxError("could not rotate an empty vector :(! ")
    a = math.cos(theta / 2.0)
    b, c, d = -normalised_axis * math.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])





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
    
        super().__init__( pts )
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




class link_2D_shape(msp.polyhedron):
    """
        take a list of 2D shape in space and try to link them together
        to make a polyhedron
        
        this is experimental yet .... but can be usefull 
        this work only with 
    """
    def __init__(self, list_of_polygon, closed=False):
        """
        @param list_of_polygon:  a list of object of type 'polygon' or trnaslation/rotation() of wone polygon 
        @param closed  if set to true, the last polygon will loop on the first one
        """
    
    
        #check that we have at least 2 polygons ....
        if len(list_of_polygon) <=1 : 
            raise SyntaxError("must have at least 2 polygon to link together !")
        #check that all polygons have the same number of points .....

        floating_points = [self._from_shape_get_pts(b) for b in list_of_polygon]
        len_of_points = [len(b) for b in floating_points]
        for b in len_of_points:
            if b != len_of_points[0]:
                raise SyntaxError("currently link_2D_shape support only polygn with the same number of points")
        
        len_pts = len_of_points[0] # number of points per vector
        
        # now we will attribute an id for every point we got 
        points_id = [ [b+(k*len_pts) for b in range(len_pts)] for k in range(len(floating_points))]

        
        #and since openScad take an array of points ==> let's flatten all our points 
        flat_point_list = []
        for b in floating_points:
            flat_point_list.extend(b)
        
        
        #we have all ID we need .... now we can construct all surfaces :

        face = self._close_one_edge(points_id[0])
        for b in range(len(points_id)-1):
            face.extend(self._link_2_poly_together(points_id[b],  points_id[b+1]  ))
        face.extend(self._close_one_edge(points_id[-1], top =True))
        
        
        super().__init__( points =flat_point_list, faces= face )
        self.name = "polyhedron"
        
        
        
    def _close_one_edge(self, listPts, top =False):
        # letes make triangle from one pts 
        
        if not top:
            listPts= [b for b in reversed(listPts)]
        source_pts = listPts[0]
        toret =  [[ source_pts, listPts[b+2],  listPts[b+1]] for b in range(len(listPts)-2)]
        return toret
        
    def _link_2_poly_together(self, A, B): 
        # prendre A[0] puis B[0] puis B[1] puis A[1]  et again for next surface
        # always need to 'turn' in the same direction !  or no F6 generation
        # first we close the loop 
        A = A + [A[0]] 
        B = B + [B[0]]
        
        toreturn = [[ A[b] , B[b] , B[b+1] , A[b+1] ] for b in range(len(A)-1)] # was not manyfold =/
        
        return toreturn
        
    
    def _from_shape_get_pts(self, theShape):
        current = type(theShape)

        if(issubclass(current, msp.polygon)):
            pts = theShape.getPoints()
            pts = [ b + [0] for b in pts]
            return pts
            
        elif(issubclass(current, msp.rotate)):
            pts = self._from_shape_get_pts(theShape.getChilds()[0])
            rot_vect = theShape.getRotation()
            rot_vect = [math.radians(b) for b in rot_vect]
            new_pts = [np.dot(rotation_matrix(rot_vect ), kb )  for kb in pts]
            return [b for b in new_pts]

        elif(issubclass(current, msp.translate)):
            pts = self._from_shape_get_pts(theShape.getChilds()[0])
            translation_vect = theShape.getTranslation()
            toret = [None]*len(pts)
            for b in range(len(pts)):
                newPos = [ (translation_vect[k] + pts[b][k]) for k in range(len(translation_vect))  ]
                toret[b] = newPos
            return toret
  
        else : 
            raise SyntaxError("link_2D_shape does not support element of type : %s"%str(current))
        return pts