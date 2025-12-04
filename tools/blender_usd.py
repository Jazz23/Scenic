import bpy
import json
import os
import sys
import math
from mathutils import Vector

# ------------------------------------------------------------------------------
# HELPER: Compute Bounding Box Center and Dimensions
# ------------------------------------------------------------------------------
def get_bbox_center_world(obj):
    local_bbox_center = 0.125 * sum((Vector(b) for b in obj.bound_box), Vector())
    return obj.matrix_world @ local_bbox_center

def get_orientation(obj):
    # Scenic usually expects Euler angles or Quaternions. 
    # Blender uses Euler XYZ by default. Converting to list.
    return [obj.rotation_euler.x, obj.rotation_euler.y, obj.rotation_euler.z]

# ------------------------------------------------------------------------------
# MAIN PIPELINE
# ------------------------------------------------------------------------------
def process_usd(usd_path, output_folder):
    # 1. Clear existing scene
    bpy.ops.wm.read_factory_settings(use_empty=True)

    # 2. Import USD
    # Note: 'scale' options might be needed depending on your USD units
    print(f"Importing: {usd_path}...")
    bpy.ops.wm.usd_import(filepath=usd_path)

    # 3. Extract Metadata (Replicating 'get_mesh_info' from Isaac script)
    transforms = {}
    
    # Filter for mesh objects only
    scene_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    
    print(f"Analyzing {len(scene_objects)} objects...")
    
    for i, obj in enumerate(scene_objects):
        # Create a unique name (Isaac script used prim_0, prim_1...)
        unique_name = f"prop_{i}_{obj.name}"
        
        # Calculate world position (center of bbox)
        pos = get_bbox_center_world(obj)
        rot = get_orientation(obj)
        
        transforms[unique_name] = {
            "full_path": obj.name,  # Blender doesn't have USD paths, using object name
            "position": [pos.x, pos.y, pos.z],
            "orientation": rot,
            "scale": [obj.scale.x, obj.scale.y, obj.scale.z] # Added scale (useful for Scenic)
        }

    # 4. Save JSON Info
    file_name = os.path.splitext(os.path.basename(usd_path))[0]
    json_path = os.path.join(output_folder, f"{file_name}_info.json")
    
    with open(json_path, 'w') as f:
        json.dump(transforms, f, indent=2)
    print(f"Saved Metadata: {json_path}")

    # 5. Export to OBJ (The Mesh for Scenic)
    obj_path = os.path.join(output_folder, f"{file_name}.obj")
    
    # We select everything to export the whole map as one mesh region
    bpy.ops.object.select_all(action='SELECT')
    
    bpy.ops.export_scene.obj(
        filepath=obj_path,
        use_selection=True,
        axis_forward='Y',  # CARLA/Unreal uses Y-forward mostly, adjust if needed
        axis_up='Z'
    )
    print(f"Saved Mesh: {obj_path}")

# ------------------------------------------------------------------------------
# ARGUMENT PARSING
# ------------------------------------------------------------------------------
# usage: blender --background --python usd_to_obj_blender.py -- <file.usd> <output_folder>
if "--" in sys.argv:
    args = sys.argv[sys.argv.index("--") + 1:]
    if len(args) < 2:
        print("Usage: blender -b -P script.py -- <input.usd> <output_dir>")
    else:
        input_usd = args[0]
        output_dir = args[1]
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        process_usd(input_usd, output_dir)
else:
    print("No arguments found after '--'")
# ```

# #### How to run this:
# You do not need to open Blender. Run this command in your terminal:
# ```bash
# blender --background --python usd_to_obj_blender.py -- /path/to/map.usd /path/to/output_folder