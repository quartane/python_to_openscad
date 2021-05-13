from my_solid_python import *

debug_test_path = "C:/Users/snooo/Desktop/test.scad"


A = hexagon(radius = 5*cm)
A = A.linear_extrude(2*cm)
 



#---- render .....
total = A
tmp = (total.render())
print("\n\n\n\n")
with open(debug_test_path, "w") as outF:
    print(tmp)
    outF.write(tmp)



