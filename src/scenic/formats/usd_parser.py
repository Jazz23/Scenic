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
        if prim.IsA(UsdGeom.Mesh):
            mesh = UsdGeom.Mesh(prim)
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
                quat = rotation.GetQuaternion()
                qw = quat.GetReal()
                qx, qy, qz = quat.GetImaginary()
                
                # Compute Euler angles from quaternion (radians)
                sinr_cosp = 2 * (qw * qx + qy * qz)
                cosr_cosp = 1 - 2 * (qx * qx + qy * qy)
                roll = math.atan2(sinr_cosp, cosr_cosp)
                
                sinp = 2 * (qw * qy - qz * qx)
                if abs(sinp) >= 1:
                    pitch = math.copysign(math.pi / 2, sinp)  # Use 90 degrees if out of range
                else:
                    pitch = math.asin(sinp)
                
                siny_cosp = 2 * (qw * qz + qx * qy)
                cosy_cosp = 1 - 2 * (qy * qy + qz * qz)
                yaw = math.atan2(siny_cosp, cosy_cosp)
                
                # Convert to Scenic-friendly format (degrees)
                position = (translation[0], translation[2], translation[1])
                orientation = (math.degrees(yaw), math.degrees(pitch), math.degrees(roll))

                geometry_info = {
                    "name": prim.GetName(),
                    "type": "Mesh",
                    "position": position,
                    "orientation": orientation,  # (yaw, pitch, roll) in degrees
                    "width": width,
                    "length": length,
                    "height": height
                }
                geometry_data.append(geometry_info)

    return geometry_data