"""
    this is a trial to see how we can generate openscad via python in an oriented object way

"""
try :
    from . import render_openscad as render
except :
    import render_openscad as render



# ------------------ basics units ----------------------
mm = render.getmm()
cm = 10*mm
dm = 10*cm
m  = 10*dm
km = 1000*m
inch = 0.0254*m
feet = 0,3048*m

def argto_string(arg):
    if (type(arg) is tuple ) or (type(arg) is list ) :
        return "[%s]"%(", ".join([argto_string(b) for b in arg]))
    
    # ok don't know if it's a good idea ...
    # but here I'll transform every float into int 
    
    if type(arg) is str:
        return arg
    return str(int(arg))
    

 

"""
$fa
    minimum angle
$fs
    minimum size
$fn
    number of fragments
$t
    animation step
$vpr
    viewport rotation angles in degrees
$vpt
    viewport translation
$vpd
    viewport camera distance
$children
     number of module children
$preview
     true in F5 preview, false for F6 
"""
# ------------------ basics units ----------------------
class shape:
    __uid__=0
    def __init__(self):
        self.u_id = shape.__uid__
        shape.__uid__+=1
        self.child_list=[]
        self.name = None

    def __add__(self, B):
        return union(self, B)
    def union(self, B):
        return self.__add__(B)

    def __sub__(self, B):
        return difference(self, B)

    def difference(self, B):
        return self.__sub__(B)

    def __xor__(self, B):
        return intersection(self,B)

    def intersection(self, B):
        return self.__xor__(B)

    def render(self):
        return render.render(self)

    def __render__(self):
        raise NotImplementedError("must implement to render one item")

    def translate(self, x_y_z ):
        return translate(self, x_y_z)
    def translateX(self, X ):
        return translate(self, [X,0,0])
    def translateY(self, Y ):
        return translate(self, [0,Y,0])
    def translateZ(self, Z ):
        return translate(self, [0,0,Z])

    def rotate(self, x_y_z ):
        return rotate(self, x_y_z)
    def rotateX(self, X ):
        return rotate(self, [X,0,0])
    def rotateY(self, Y ):
        return rotate(self, [0,Y,0])
    def rotateZ(self, Z ):
        return rotate(self, [0,0,Z])

    def scale(self, x_y_z ):
        return scale(self, x_y_z)
    def scaleX(self, X ):
        return scale(self, [X,0,0])
    def scaleY(self, Y ):
        return scale(self, [0,Y,0])
    def scaleZ(self, Z ):
        return scale(self, [0,0,Z])

    def resize(self, x_y_z ):
        return resize(self, x_y_z)
    def resizeX(self, X ):
        return resize(self, [X,0,0])
    def resizeY(self, Y ):
        return resize(self, [0,Y,0])
    def resizeZ(self, Z ):
        return resize(self, [0,0,Z])


    def linear_extrude( self, height=None,center=False,convexity=None,twist=None,slices=None):
        return linear_extrude(self, height=height, center=center, convexity=convexity, twist=twist,slices=slices)

    def rotate_extrude( self, angle,convexity=None):
        return rotate_extrude(self, angle=angle, convexity=convexity)

    #----- rendering a shape : basic concept ----

    def render_name(self):
        """
        @brief return the name of the module if nothings specified....
        """
        if self.name is None:
            return type(self).__name__
        return self.name

    def render_args(self):
        raise NotImplementedError("render_args for  %s must be implemented "%type(self))

    def get_childs_to_render(self):
        if len(self.child_list) ==0:
            return None
        return self.child_list

    def color(self, colorn, alpha=None):
        return color(self, colorn=colorn,alpha=alpha)
    
    # def hole(self):
        # return hole(self)
    
    # def part(self):
        # return part(self)





# class hole(shape):
    # """
        # special object that will not render himself, 
        # but everything placed inside  will dig a hole 
        # in the final parts 
        # the hole is nulified with the part Object :)
    # """
    # def __init__(self):
        # super().__init__()
    
    # def render(self, list_hole = None):
        # if list_hole is None:
            # raise SyntaxError("To use hole, parent must be a 'part'!")
        # list_hole.append(self)
        # return ""
    
    # def render_hole(): 
        # will not work since we have to translate rotate, .... hole ... we can't just put the out this 
        # toreturn = "" 
        # for b in child_list:
            # toreturn+=b.render()
        # return toreturn
        
# class part(shape):
    # def __init__(self):
        # super().__init__()

    # def render(self,list_hole=None):
        # my_list_hole = []
        # toreturn = "" 
        # for b in child_list:
            # toreturn+=b.render(list_hole = my_list_hole)
        # return toreturn



class advanced_shape(shape):
    def __init__(self):
        super().__init__()
        self.child_list.append( self._draw_myself_())
        
    def _draw_myself_(self):
        raise SyntaxError("advanced_shape object or child must define thier _draw_myself_ method")
    
    def render(self):
        return render.render(self.child_list[0])


#------------------------ basics shape --------------------------------------
class sphere(shape):
    """
    sphere(radius | d=diameter)
    """
    def __init__(self, radius=None, d=None, diameter = None):
        super().__init__()
        total = sum( [ 1 if b else 0 for b in [radius, d, diameter] ]  )
        if total != 1 :
            raise SyntaxError("sphere: only one arg can be specified : radius, diameter=d")
        self.radius   = radius
        self.diameter = d
        if diameter:
            self.diameter = diameter

    def render_args(self):
        if self.radius:
            return "r=%s "%argto_string(self.radius)
        if self.diameter:
            return "d=%s "%argto_string(self.diameter)
        if self.d:
            return "d=%s "%argto_string(self.d)
        return argto_string(self.size)


class cube(shape):
    """
    cube(size, center)
    cube([width,depth,height], center)
    """
    def __init__(self, size=None, center = False):
        super().__init__()
        if size is None :
            raise SyntaxError("Cube must have a size!")
        self.size   = size
        self.center = center

    def render_args(self):
        if self.center:
            return argto_string(self.size) +","+"center=true"
        return argto_string(self.size)



class cylinder(shape):
    """
    cylinder(h,r|d,center)
    cylinder(h,r1|d1,r2|d2,center)
    """

    def __init__(self,h =None, height=None,  r=None, radius=None, d=None, diameter=None, center = False, r1=None, r2=None, d1=None, d2=None):
        super().__init__()
     
        if (not h) and (not height):
            raise SyntaxError("cylinder must have a heigth ")
            
            
        total_cylinder = sum( [ 1 if b else 0 for b in [r, radius, d, diameter] ]  )
        
        total_cone     = sum( [ 1 if b else 0 for b in [r1, r2, d1, d2] ]  )
        
        if not ( 
            (total_cylinder == 0 and  total_cone == 2)or 
            (total_cylinder == 1 and  total_cone == 0)) :
             
            raise SyntaxError("""
          when using cylinder, one must define either 
          [  radius |  diameter |  d1 and d2  | r1 and r2 ]
          any other combinaison will be refused ...
            """)
        
         
        self.height = h if h else height
        self.radius = None
        self.diameter = None
        self.r1 = r1
        self.r2 = r2
        self.d1 = d1
        self.d2 = d2
        if r:
            self.radius = r
        if d:
            self.diameter = d
        self.center = center
       
    def render(self):
        return super().render()

    def render_args(self):
        heigth_args = "h=%s, "%( argto_string( self.height ) )
        center = ", center=true" if  self.center else ""
        if self.radius :
            return heigth_args + "r=%s %s"%(argto_string(self.radius),center)
        if self.diameter:
            return heigth_args + "d=%s %s"%(argto_string(self.diameter),center)
        if self.r1:
            base_1 = "r1=%s, "%argto_string(self.r1)
        if self.r2:
            base_2 = "r2=%s "%argto_string(self.r2)
        if self.d1:
            base_1 = "d1=%s, "%argto_string(self.d1)
        if self.d2:
            base_2 = "d2=%s "%argto_string(self.d2)
        return  heigth_args + base_1 + base_2 + center



class polyhedron(shape):
    """
    polyhedron(points, faces, convexity)
    """

    def __init__(self,points=None, faces=None, convexity=None):
        super().__init__()
        self.points     = points
        self.faces      = faces
        self.convexity  = convexity


"""
TODO
    import("….ext")  # TODO
    surface(file = "….ext",center,convexity) # TODO
"""


class linear_extrude(shape):
    def __init__(self, shape_obj,  height=None, center=False, convexity=None, twist=None, slices=None):
        super().__init__()
        if not issubclass(type(shape_obj), shape):
            raise SyntaxError("your trying to extrude somethings that is not a shape!")
        self.child_list.append(shape_obj)
        self.height     = height
        self.center     = center
        self.convexity  = convexity
        self.twist      = twist
        self.slices     = slices

    def render_args(self):
        toret="height=%s"%argto_string(self.height)
        if self.center:
           toret+= ", center=true"
        if self.convexity:
           toret+= ", convexity=%s"%argto_string(convexity) 
        if self.twist:
           toret+= ", twist=%s"%argto_string(twist) 
        if self.slices:
           toret+= ", slices=%s"%argto_string(slices) 
        return toret
        
        
    
class rotate_extrude(shape):
    def __init__(self, shape_obj, points=None, faces=None, convexity=None):
        super().__init__()
        if not issubclass(type(shape_obj), shape):
            raise SyntaxError("your trying to extrude somethings that is not a 2D shape!")
        self.child_list.append(shape_obj)
        self.points     = points
        self.faces      = faces
        self.convexity  = convexity
        
    def render_args(self):
        toret="height=%s"%argto_string(self.height)
 
        if self.points:
           toret+= ", points=%s"%argto_string(points) 
        if self.faces:
           toret+= ", faces=%s"%argto_string(faces) 
        if self.convexity:
           toret+= ", convexity=%s"%argto_string(convexity) 
        return toret

#------------------------ basic shape 2D -------------------------------4
"""
circle(radius | d=diameter)
square(size,center)
square([width,height],center)
polygon([points])
polygon([points],[paths])
text(t, size, font,
     halign, valign, spacing,
     direction, language, script)
import("….ext")
projection(cut)

"""
class circle(shape):
    def __init__(self, r=None, radius=None, d=None, diameter = None):
        super().__init__()
        total = sum( [ 1 if b else 0 for b in [r, radius, d, diameter] ]  )
        if total != 1 :
            raise SyntaxError("sphere: only one arg can be specified : radius, diameter=d")
        self.radius= r
        if radius:
            self.radius= radius
        self.diameter= d
        if diameter:
            self.diameter= diameter

    def render_args(self):
        if self.diameter:
            return "d=%s "%argto_string(self.diameter)
        return "r=%s "%argto_string(self.radius)


class square(shape):
    def __init__(self, size , center=False):
        super().__init__()
        self.size = size
        self.center = center
        
    def render_args(self):
        if self.center:
            return argto_string(self.size)+", center=true"
        return argto_string(self.size)


class polygon(shape):
    def __init__(self, points , path=None):
        super().__init__()
        self.points = points
        self.path = path

    def render_args(self):
        return argto_string(self.points)


class text(shape):
    def __init__(self, t, size=None, font=None, halign=None, valign=None, spacing=None,  direction=None, language=None, scrip=None):
        super().__init__()
        self.text = t
        self.size = size
        self.font = font
        self.halign = halign
        self.valign = valign
        self.spacing = spacing
        self.direction = direction
        self.language = language
        self.scrip = scrip

    def render_args(self):
        return argto_string(self.points)


class import_(shape):
    def __init__(self, obj, cut):
        super().__init__()
        self.name = "import"
        self.cut = cut

        if not issubclass(type(obj), shape):
            raise IOError("invalid object '%s' of type %s"%(str(shape), str(type(shape))))

        self.child_list.append(obj)


#---------------------------------- Transformations----------------------------
"""
mirror([x,y,z])
multmatrix(m)

offset(r|delta,chamfer)
hull()
minkowski()

"""
class translate(shape):
    # translate([x,y,z])
    def __init__(self, child, direction):
        super().__init__()
        self.child_list.append( child)
        self.direction = direction
    def render_args(self):
        return argto_string(self.direction)



class rotate(shape):
    # rotate([x,y,z])
    # rotate(a, [x,y,z]) # TODO help rotation with strange vector ...
    def __init__(self, child, x_y_z):
        super().__init__()
        self.child_list.append( child)
        self.direction = x_y_z
    def render_args(self):
        return argto_string(self.direction)



class scale(shape):
    def __init__(self, child, x_y_z):
        super().__init__()
        self.child_list.append( child)
        self.direction  = x_y_z
    def render_args(self):
        return argto_string(self.direction)


class resize(shape):
    def __init__(self, child, x_y_z, auto = None):
        super().__init__()
        self.child_list.append( child)
        self.direction  = x_y_z
        self.auto = auto
    def render_args(self):
        if not self.auto:
            return argto_string(self.direction)
        return argto_string(self.direction)+", "+argto_string(self.auto)

class color(shape):
    """
    color("colorname",alpha)
    color("#hexvalue")
    color([r,g,b,a])
    """
    def __init__(self, child, colorn, alpha=None):
        super().__init__()
        self.child_list.append(child)
        self.color = colorn
        self.alpha = alpha
       
    def render_args(self):
        if self.alpha:
            return str(self.color)+", "+argto_string(self.alpha)
        return str(self.color)

    
#------------------------ operator --------------------------------------
class union(shape):
    def __init__(self, *args):
        super().__init__()
        if len(args) < 1 :
            print(args)
            raise IOError("'union' object must at leaste have one element")
        for arg in args:
                self.__add__(arg)

    def __add__(self, B):
        if not issubclass(type(B), shape):
            raise IOError("invalid object '%s' of type  %s"%(str(shape), str(type(shape))))
        self.child_list.append(B)
        return self

    def render_args(self):
        return ""


class intersection(shape):
    def __init__(self, *args):
        super().__init__()
        if len(args) < 1 :
            raise IOError("'intersection' object must at leaste have one element")

        for arg in args:
                self.__xor__(arg)

    def __xor__(self, B):
        if not issubclass(type(B), shape):
            raise IOError("invalid object '%s' of type  %s"%(str(shape), str(type(shape))))
        self.child_list.append(B)
        return self

    def render_args(self):
        return ""


class difference(shape):
    def __init__(self, *args):
        super().__init__()

        if len(args) < 1 :
            raise IOError("'difference' object must at leaste have one element")

        self.child_list.append(args[0])
        if len(args) > 1 :
            for b in args[1:]:
                self.__sub__(b)

    def __sub__(self, B):
        if not issubclass(type(B), shape):
            raise IOError("invalid object '%s' of type  %s"%(str(shape), str(type(shape))))
        self.child_list.append(B)
        return self
        
    def render_args(self):
        return ""



 