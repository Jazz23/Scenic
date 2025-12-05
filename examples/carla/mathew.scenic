import trimesh 
from scenic.core.regions import MeshVolumeRegion
from scenic.core.shapes import MeshShape, BoxShape
from scenic.core.object_types import Object, Constructible
from scenic.core.utils import repairMesh

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

        mesh = repairMesh(mesh)
        # test = new Object at loc
                # with shape MeshShape(mesh)
                # with shape BoxShape(dimensions=(mesh.extents[1], mesh.extents[0], mesh.extents[2]))
                #  with length mesh.extents[0],
                #  with width mesh.extents[1],
                #  with height mesh.extents[2]

        # globals()[name] = test at loc

        break
        
chair = new Object at (4,0,2),
	            with shape MeshShape.fromFile(localPath("meshes/chair.obj"),
	                initial_rotation=(0,90 deg,0), dimensions=(1,1,1))
ego = new Car 