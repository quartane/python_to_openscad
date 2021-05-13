"""
  make a bridge between python and openscad :)!
  this is this part who must generate the openscad 


"""


def getmm():
    return 100
    
    

def render(obj, __tab_level=0):
    curTab = "\t"*__tab_level
    
    toreturn = curTab+"%s(%s)"%(obj.render_name() , obj.render_args())    
    listChild = obj.get_childs_to_render()
    
    if listChild:
        toadd = curTab+"{\n"
        for b in listChild:
            toadd+=render(b, __tab_level+1)
        toadd += curTab+"}"
        toreturn+=toadd
    toreturn+=";\n"
    return toreturn
    
    
    
    
    