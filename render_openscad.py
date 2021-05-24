"""
  make a bridge between python and openscad :)!
  this is this part who must generate the openscad 


"""



TABULATION_SYMBOL = "  "

def getmm():
    return 100
    

__tab_level = 0
def render(obj, first_object = False):
    global TABULATION_SYMBOL
    global __tab_level
    curTab = TABULATION_SYMBOL*__tab_level

    try:
        toreturn = curTab+"%s(%s)"%(str(obj.render_name()) , str(obj.render_args()))    
    except Exception as e:
        print("could not render %s"%(str(type(obj))))
        raise e
    listChild = obj.get_childs_to_render()
    
    if listChild:
        toadd = "\n%s{\n"%curTab
        for b in listChild:
            __tab_level+=1
            try:
                toadd+=b.__render__(  )
            except Exception as e:
                print("could not render %s"%(str(type(b))))
                raise e
            __tab_level-=1
        toadd += curTab+"}"
        toreturn+=toadd
    toreturn+=";\n"
    return toreturn
    
    
    
    
    