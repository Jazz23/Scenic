import trimesh 
from scenic.core.regions import MeshVolumeRegion
from scenic.core.shapes import MeshShape
from scenic.core.object_types import Object


city_mesh = trimesh.load('../../assets/Town1.glb')
for name, mesh in city_mesh.geometry.items():
    if "Bl_House_AmerSuburb009_N10" == name:
        print(name)
        print(mesh.volume)
        print(mesh.extents)
        print(mesh.centroid)
        print(mesh.is_volume)
        center = mesh.centroid
        # loc = float(center[0]) @ float(center[1]) 

        # test = MeshShape(mesh) 
        test = Object._with(width=mesh.extents[0], length=mesh.extents[1]) 
        globals()[name] = test 

        break



print('done')
exit()

mesh_data = trimesh.load(
    '../../assets/Town01_Opt.obj',
    split_object=True,
    group_material=False,
    process=False # Don't auto-cleanup/rename things
)

print(f"Type of loaded data: {type(mesh_data)}")

if isinstance(mesh_data, trimesh.Scene):
    print(f"Found {len(mesh_data.geometry)} unique meshes.")
    print("First 10 Mesh Names:")
    for i, name in enumerate(mesh_data.geometry.keys()):
        print(f"  - {name}")
else:
    print("Loaded as a single mesh (Names lost).")

exit()

print("shouldn't be here")
scene_data = trimesh.load(str("../../assets/Town01_Opt.obj"))

for name, mesh in scene_data.geometry.items():
    print(name)

print("done")
