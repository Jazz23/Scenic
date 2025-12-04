import bpy
import os
import sys
import addon_utils

def enable_usd_addon():
    """Force enable the USD IO addon."""
    addon_name = "io_scene_usd"
    loaded, _ = addon_utils.check(addon_name)
    if not loaded:
        print(f"Enabling addon: {addon_name}...")
        addon_utils.enable(addon_name, default_set=True)
    else:
        print(f"Addon {addon_name} already enabled.")

def import_usd_safe(filepath):
    """Try multiple import commands depending on Blender version."""
    print(f"Attempting to import: {filepath}")
    
    # # Method 1: Modern Blender (4.0+)
    # if hasattr(bpy.ops.wm, "usd_import"):
    #     print("Using: bpy.ops.wm.usd_import")
    #     bpy.ops.wm.usd_import(filepath=filepath)
    #     return

    # # Method 2: Older Blender (3.x)
    # if hasattr(bpy.ops.import_scene, "usd"):
    #     print("Using: bpy.ops.import_scene.usd")
    bpy.ops.import_scene.usd(filepath=filepath)
    return

    # Fail state
    print("ERROR: No USD import operator found.")
    print("Your Blender version is likely too old (< 3.0).")
    print("Please download a newer version from https://builder.blender.org/download/")
    sys.exit(1)

def process_usd(usd_path, output_folder):
    # Clear scene
    bpy.ops.wm.read_factory_settings(use_empty=True)
    
    # Force Enable Addon
    try:
        enable_usd_addon()
    except Exception as e:
        print(f"Warning: Could not enable USD addon: {e}")

    # Import
    import_usd_safe(usd_path)

    # Export Info (JSON)
    scene_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    import json
    from mathutils import Vector
    
    transforms = {}
    for i, obj in enumerate(scene_objects):
        # Calculate center
        local_bbox_center = 0.125 * sum((Vector(b) for b in obj.bound_box), Vector())
        pos = obj.matrix_world @ local_bbox_center
        rot = [obj.rotation_euler.x, obj.rotation_euler.y, obj.rotation_euler.z]
        
        # Use object name as key
        transforms[obj.name] = {
            "full_path": obj.name,
            "position": [pos.x, pos.y, pos.z],
            "orientation": rot,
            "scale": [obj.scale.x, obj.scale.y, obj.scale.z]
        }

    # Save JSON
    file_name = os.path.splitext(os.path.basename(usd_path))[0]
    json_path = os.path.join(output_folder, f"{file_name}_info.json")
    with open(json_path, 'w') as f:
        json.dump(transforms, f, indent=2)
    print(f"Saved Metadata: {json_path}")

    # Export OBJ
    obj_path = os.path.join(output_folder, f"{file_name}.obj")
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.obj(
        filepath=obj_path,
        use_selection=True,
        axis_forward='Y',
        axis_up='Z'
    )
    print(f"Saved Mesh: {obj_path}")

if __name__ == "__main__":
    # blender --background --python script.py -- <input> <output>
    if "--" in sys.argv:
        args = sys.argv[sys.argv.index("--") + 1:]
        if len(args) < 2:
            print("Usage: blender -b -P script.py -- <input.usd> <output_dir>")
            sys.exit(1)
            
        process_usd(args[0], args[1])
    else:
        print("No arguments found. Use '--' to separate arguments.")