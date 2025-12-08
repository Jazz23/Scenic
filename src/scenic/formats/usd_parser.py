from pxr import Usd, UsdGeom, Gf
import trimesh
import math  # For degrees conversion
from scenic.core.utils import repairMesh

def parse_usd_file(file_path):
    stage = Usd.Stage.Open(file_path)
    if not stage:
        raise ValueError(f"Could not open USD file: {file_path}")

    geometry_data = []

    for prim in stage.Traverse():
        if (not prim.IsA(UsdGeom.Mesh)) and (not prim.IsA(UsdGeom.Xform)):
            continue
        
        targetPrim = None
        if prim.IsA(UsdGeom.Mesh):
            targetPrim = prim
        elif prim.IsA(UsdGeom.Xform):
            targetPrim = prim.GetChild("LOD0")
            
        if targetPrim is None or not targetPrim.IsValid():
            continue
        
        mesh = UsdGeom.Mesh(targetPrim)
        points_attr = mesh.GetPointsAttr()
        points = points_attr.Get()

        # Get face indices (triangles or polygons)
        face_counts = mesh.GetFaceVertexCountsAttr().Get()
        face_indices = mesh.GetFaceVertexIndicesAttr().Get()

        if points is not None and face_indices is not None:
            # Convert to trimesh-compatible format (assuming triangles)
            faces = []
            idx = 0
            for count in face_counts:
                if count == 3:  # Triangle
                    faces.append([face_indices[idx], face_indices[idx+1], face_indices[idx+2]])
                # Handle quads or other polygons if needed (triangulate)
                idx += count

            # Create trimesh object
            trimesh_mesh = trimesh.Trimesh(vertices=points, faces=faces)

            # Compute bounding box dimensions
            bounds = trimesh_mesh.bounds
            min_bounds = bounds[0]
            max_bounds = bounds[1]
            width = max(max_bounds[0] - min_bounds[0], 0.1)
            length = max(max_bounds[1] - min_bounds[1], 0.1)
            height = max(max_bounds[2] - min_bounds[2], 0.1)

            # Extract position and orientation from transform
            xformable = UsdGeom.Xformable(prim)
            transform = xformable.ComputeLocalToWorldTransform(Usd.TimeCode.Default())
            
            # Decompose transform: translation and rotation
            translation = transform.ExtractTranslation()
            rotation = transform.ExtractRotation()
            
            x_scalar = 100.0034018362
            y_scalar = -100.0454723616
            
            position = ((translation[0]+6.4340926549) / x_scalar, (translation[2]+7.8286226668) / y_scalar, translation[1])
            orientation = (rotation.angle + math.pi - 0.2, 0, 0)#-rotation.angle)

            geometry_info = {
                "name": prim.GetName(),
                "type": "Mesh",
                "position": position,
                "orientation": orientation,  # (yaw, pitch, roll) in degrees
                "width": width / x_scalar,
                "length": length / -y_scalar,
                "height": height
            }
            geometry_data.append(geometry_info)

    return geometry_data