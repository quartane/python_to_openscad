"""
    define a global variable that can be used for openscad

"""

def get_list_of_globals_variable():
    """
        return all object of type global_variable  
        that were created without the _do_not_add_ argument set to True.
        
        this allow to generate a header to the openscad file.
    """
    return global_variable.list_of_globals_defined[:]


def activate_render_mode(  activated = False):
        """
            value returned wont be anymore scalar value but string if True
        """
        global_variable.__render_mode = activated



class global_variable:
    """
      global variable aim to create variable that user can change inside the .scad file directly 
      without passing via python. 
      
    
    """


    list_of_globals_defined=[] # list all global variable that exist!
    __render_mode = False #as long as false ==> returned value are scalar  for operation 
    
    
    
    def __init__(self, name, value, description=None, force_present = False, _do_not_add_ = False):
        """
        name : the name to print inside the global value 
        value : the value the variable take (can be operation with other global_variable)
        description : the comment text after the declaration of the variable
        force_present: by default, if a variable is not used, she is not printed either  ... with this to True she will
        
        """
        
        self.activate_render_mode(True)
        if type(name) != str: 
            raise SyntaxError("global variable name must be string!")
        self.name = name
        
        self.value = value
        self.description = description
        self.force_present = force_present

        if not _do_not_add_:
            for k in global_variable.list_of_globals_defined:
                if(k.getName()  == self.getName()):
                    raise(SyntaxError("global variable with this name already exist!"))
            global_variable.list_of_globals_defined.append(self)
        
        self.this_variable_is_used_in_the_code  = False
        self.numberOfOccuranceInCode = 0
        self.activate_render_mode(False)

    def activate_render_mode(self, activated = False):
        """
            change the behavior of this object!  
            if True : the object will return a tree of object contening operation to find the value 
            if False : the object will return scalar value for operation! 
            
            this allow to use the object in for loop or if else inside the code  while keeping 
            the freedom to have a global variable in the gerated code ! 
            still it's not recomended since some case can lead to unpredicted behavior...
            but hey :), you have this possibility, up to you to try it.
        """
        global_variable.__render_mode = activated
    
    
    def is_used_in_the_code(self):
        """
            return whenever this variable is used inside the code or not.
            // TODO ==> recursive check if called inside an object somwhere
            // curently we just check if str is called once
        """

        return self.this_variable_is_used_in_the_code
    
    def getString(self):
        """
            return a string representation of this variable, 
            relative to others globals variable.
            for example if this is an basic_operation 10*cm 
            will return "(10*cm)"
            if this is just a variable, will return the variable name ...
        """
        returnToRender = global_variable.__render_mode
        self.activate_render_mode(True)
        toreturn = str(self)
        self.activate_render_mode(returnToRender)
        #ensure we don't think the variable is used if we call getString()
        if type(self) is global_variable:
            self.numberOfOccuranceInCode-=1 
        return toreturn
        
        
    def getScalar(self):
        """
            return a scalar value for this variable
        """
        if issubclass(type(self.value), global_variable):
            return self.value.getScalar()
        return str(self.value)
        
        
        
    def getName(self):
        """
            return the name of this variable 
        """
        return str(self.name)

    def render(self):
        """
            return a variable then a description inside the header of the 
            .scad file ! 
        """
        if not self.is_used_in_the_code() or self.force_present:
            return ""

        toret = "%s = %s;"%(self.getName(),str(self.value))
        if(self.description):
           toret +="/*%s*/"%str(self.description)
        return toret+"\n"
    
    def check_used(self):
        """
            Check if the global variable is used inside the code 
            if yes, pass all variable and itself as 'used' 
            it mean it will generated inside the header of the 
            .scad file
        """
        if self.numberOfOccuranceInCode > 0:
            self.set_used()

    def set_used(self):
        """
            set this variable as used and all variable that compose it ...
            it mean the header of the scad file will have this variable 
             
        """
        
        self.this_variable_is_used_in_the_code  = True
        if issubclass(type(self.value), global_variable):
            self.value.set_used()

# overloading operation
    
    def return_basic_operation(self, A, B, operation):
        """
            return an object of type basic_operation if activate_render_mode is set to True
            else will return a scalar value of this object.
        """
        if global_variable.__render_mode:
            return basic_operation(A,  B, operation)
        else : 
            return basic_operation(A,  B, operation).getScalar()
        
    def __str__(self):
        self.numberOfOccuranceInCode+=1
        return str(self.name)

    def __add__(self, p2): # Addition
        return self.return_basic_operation(self,  p2, "+")
    def __radd__( p2,self):
        return self.return_basic_operation(self,  p2, "+")
    def __sub__(self, p2) :# Subtraction
        return self.return_basic_operation(self,  p2, "-")
    def __rsub__( p2, self) :# Subtraction
        return self.return_basic_operation(self,  p2, "-")
    def __mul__(self, p2) :# Multiplication
        return self.return_basic_operation(self,  p2, "*")
    def __rmul__( self, p2) :# Multiplication
        return self.return_basic_operation(self,  p2, "*")
    def __pow__(self, p2) :# Power
        raise NotImplementedError("power (^) is not yet impelmented for global variable ")
    def __rpow__( p2, self) :# Power
        raise NotImplementedError("power (^) is not yet impelmented for global variable ")
    def __truediv__(self, p2) :# Division
        return self.return_basic_operation(self,  p2, "/")
    def __rtruediv__( p2,self) :# Division
        return self.return_basic_operation(self,  p2, "/")
    def __floordiv__(self, p2) :# Floor Division
        raise NotImplementedError("floor div (//) is not yet impelmented for global variable ")
    def __rfloordiv__( p2,self) :# Floor Division
        raise NotImplementedError("floor div (//) is not yet impelmented for global variable ")
    def __mod__(self, p2) :# Remainder (modulo)
        return self.return_basic_operation(self,  p2, "%")
    def __rmod__( p2,self) :# Remainder (modulo)
        return self.return_basic_operation(self,  p2, "%")
    def __lshift__(self, p2) :# Bitwise Left Shift
        raise NotImplementedError("Left shift (//) is not yet impelmented for global variable ")
    def __rlshift__( p2,self) :# Bitwise Left Shift
        raise NotImplementedError("Left shift (//) is not yet impelmented for global variable ")
    def __rshift__(self, p2) :# Bitwise Right Shift
        raise NotImplementedError("Right shift (//) is not yet impelmented for global variable ")
    def __rrshift__( p2, self) :# Bitwise Right Shift
        raise NotImplementedError("Right shift (//) is not yet impelmented for global variable ")
    def __and__(self, p2) :# Bitwise AND
        return self.return_basic_operation(self,  p2, "&")
    def __rand__( p2, self) :# Bitwise AND
        return self.return_basic_operation(self,  p2, "&")
    def __or__(self, p2) :# Bitwise OR
        return self.return_basic_operation(self,  p2, "|")
    def __ror__( p2, self) :# Bitwise OR
        return self.return_basic_operation(self,  p2, "|")
    def __xor__(self, p2) :# Bitwise XOR
        return self.return_basic_operation(self,  p2, "^")
    def __rxor__( p2,self) :# Bitwise XOR
        return self.return_basic_operation(self,  p2, "^")
    def __invert__(self) :# Bitwise NOT
        raise NotImplementedError("Invert is not yet implemented for global_variable object")
    def __lt__(self, p2):# Less than
        return self.return_basic_operation(self,  p2, "<")
    def __rlt__( p2, self):# Less than
        return self.return_basic_operation(self,  p2, "<")
    def __le__(self, p2):# Less than or equal to
        return self.return_basic_operation(self,  p2, "<=")
    def __rle__( p2, self):# Less than or equal to
        return self.return_basic_operation(self,  p2, "<=")
    def __eq__(self, p2):# Equal to
        return self.return_basic_operation(self,  p2, "==")
    def __req__( p2, self):# Equal to
        return self.return_basic_operation(self,  p2, "==")
    def __ne__(self, p2):# Not equal to
        return self.return_basic_operation(self,  p2, "!=")
    def __rne__( p2, self):# Not equal to
        return self.return_basic_operation(self,  p2, "!=")
    def __gt__(self, p2):# Greater than
        return self.return_basic_operation(self,  p2, ">")
    def __rgt__( p2, self):# Greater than
        return self.return_basic_operation(self,  p2, ">")
    def __ge__(self, p2):# Greater than or equal to
        return self.return_basic_operation(self,  p2, ">=")
    def __rge__( p2, self):# Greater than or equal to
        return self.return_basic_operation(self,  p2, ">=")
    def __neg__(self):
        self.return_basic_operation(0, self, "-")
        return self
        
class basic_operation(global_variable):
    accepted_operation = [
         "+","-","*","/", "//","%",
         "&","|","^",
         "<","<=","==","!=",">",">="
        ] # for security reason we won't allow executing other operation than thoses ...
        # because we use "eval" function don't know if you can execute custom code ...
        # but why risk it ? 
        
    def __init__(self, A, B , operation ):
        """
            A: the first operand of the operation
            B: the second operand of the operation
            operation : the operation you want to perform!
        """
        self.activate_render_mode(True)
        self.A = A
        self.B = B
        self.operation = operation
        super().__init__("","", _do_not_add_=True)
        self.activate_render_mode(False)

    
    def getScalar(self):
        """
            return the value of the operation ...
        """
        if not self.operation in basic_operation.accepted_operation:
            raise SyntaxError("can't get scalar value for operation : %s! not in allowed operations"%str(self.operation))
        
        A= str(self.A.getScalar()) if  issubclass(type(self.A),global_variable ) else str(self.A)
        B= str(self.B.getScalar()) if  issubclass(type(self.B),global_variable ) else str(self.B)
          
        toreturn = eval("(%s%s%s)"%(A,self.operation, B))
        return toreturn
        
        
        
    def set_used(self):
        """
            tell to this variable and all his "parent" that they are used 
            and so you have to display it inside the "header" of the openscad output
        """
        for k in [self.A, self.B, self.operation]:
            if(issubclass(type(k),global_variable )):
                k.set_used()
        
    def __str__(self):
        return "(%s%s%s)"%( str(self.A), self.operation, str(self.B))