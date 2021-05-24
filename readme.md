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

FA = global_variable("$fa", 0.5, "render more detailled circles", force_present=True)
A = global_variable("A", 1*mm, "variable A description")

# create a cube and a sphere and make a union of them
A = cube([A, 2*A, 3*A])+ sphere(radius=1*dm).translateZ(1*dm)
#rotate the whole structure
A = A.rotateZ(76)
#print into the console the openscad result
print(A.render())
```



# TODO
 - implement the remaining of the openscad syntaxe
 - support for holes and parts [if I have time]
 - doc 
