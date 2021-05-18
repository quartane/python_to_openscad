# python to openscad

this is an under developpement project that aim to produce openscad code from python code oriented object


# install 
there is no installation procedure yet.  but since it's pure python, you just have to submodule on the root of your project.
if the project is a valid git repo : 

```git submodule add git@github.com:quartane/python_to_openscad.git```

then inside the code , you just have to 

```
from python_to_openscad.python_to_openscad import * 


```


# example

```
from python_to_openscad.python_to_openscad import * 

# create a cube and a sphere and make a union of them
A = cube([1*cm,3*cm,5*cm])+ sphere(radius=1*dm).translateZ(1*dm)
#rotate the whole structure
A = A.rotateZ(76)
#print into the console the openscad result
print(A.render())
```



# TODO
 - implement the remaining of the openscad syntaxe
 - add _global_ variable :  variable that you can modify later inside 
 - support for holes and parts [if I have time]
 - doc 
