import gmsh
import numpy as np

gmsh.initialize()
factory = gmsh.model.occ

model_name = "cylinder_pi"
gmsh.model.add(model_name)

# CR20216 battery
CR2016_diameter = 2*np.sqrt(1/np.pi)
CR2016_thickness =3

# Cylinder
cyl = factory.addCylinder(0, 0, 0, 0, 0, CR2016_thickness, 0.5 * CR2016_diameter)

# Slice in fractions of thickness
xvals = [1/3, 2/3]
planes = [
    factory.addRectangle(
        -CR2016_diameter,
        -CR2016_diameter,
        xval * CR2016_thickness,
        2 * CR2016_diameter,
        2 * CR2016_diameter,
    )
    for xval in xvals
]

# Split the cylinder
factory.synchronize()
cyl_dt = [(3, cyl)]
planes_dt = [(2, plane) for plane in planes]
dt, dt_map = factory.fragment(cyl_dt, planes_dt)

# Remove all 2D objects
factory.synchronize()
to_remove = []
for o in dt:
    if o[0] == 2:
        to_remove.append(o)
factory.remove(to_remove)

# Mesh
factory.synchronize()
#gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 20)
gmsh.option.setNumber("Mesh.MeshSizeMax", 0.1)
gmsh.model.mesh.generate(3)

# Dump
gmsh.write(model_name + ".msh")
gmsh.write(model_name + ".mesh")
gmsh.finalize()
