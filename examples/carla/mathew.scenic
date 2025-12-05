import trimesh 
from scenic.core.regions import MeshVolumeRegion
from scenic.core.shapes import MeshShape
from scenic.core.object_types import Object

param map = localPath('../../assets/maps/CARLA/Town01.xodr')
model scenic.simulators.carla.model

test = ""

city_mesh = trimesh.load(localPath('../../assets/Town1.glb'))
for name, mesh in city_mesh.geometry.items():
    if "Bl_House_AmerSuburb009_N10" == name:
        print(name)
        print(mesh.volume)
        print(mesh.extents)
        print(mesh.centroid)
        center = mesh.centroid
        loc = center[0] @ center[1] @ center[2]

        # test = MeshShape(mesh) 
        # test = Object._with(length=mesh.extents[0], width=mesh.extents[1], height=mesh.extents[2]) 

        test = new Object at loc,
                with shape BoxShape()
                #  with length mesh.extents[0],
                #  with width mesh.extents[1],
                #  with height mesh.extents[2]

        # globals()[name] = test at loc

        break

ego = new Car 