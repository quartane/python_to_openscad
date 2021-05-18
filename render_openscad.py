"""
  make a bridge between python and openscad :)!
  this is this part who must generate the openscad 


"""


def getmm():
    return 100
    

__tab_level = 0
def render(obj):
    global __tab_level
     
    curTab = "\t"*__tab_level
    
    try:

        toreturn = curTab+"%s(%s)"%(str(obj.render_name()) , str(obj.render_args()))    
    except Exception as e:
        print("could not render %s"%(str(type(obj))))
        raise e
    listChild = obj.get_childs_to_render()
    
    if listChild:
        toadd = curTab+"{\n"
        for b in listChild:
            __tab_level+=1
            try:
                toadd+=b.render(  )
            except Exception as e:
                print("could not render %s"%(str(type(b))))
                raise e
            __tab_level-=1
        toadd += curTab+"}"
        toreturn+=toadd
    toreturn+=";\n"
    return toreturn
    
    
    
    
    