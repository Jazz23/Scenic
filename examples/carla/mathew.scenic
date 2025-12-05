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
        loc = float(center[0]) @ float(center[1]) 

        # test = MeshShape(mesh) 
        test = Object._with(width=mesh.extents[0], length=mesh.extents[1]) 
        globals()[name] = test 

        break

ego = new Car left of test by 5