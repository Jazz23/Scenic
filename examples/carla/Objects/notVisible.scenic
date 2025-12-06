'''
To run this file using the Carla simulator:
    scenic examples/carla/car.scenic --2d --model scenic.simulators.carla.model --simulate
'''
from scenic.formats.usd_parser import parse_usd_file
from scenic.core.regions import AllRegion
import scenic.simulators.carla.blueprints as blueprints

param map = localPath('../../../assets/maps/CARLA/Town01.xodr')
model scenic.simulators.carla.model

# Load USD data (run at compile time)
usd_data = parse_usd_file("G:\Desktop\Town01_Opt.usd")

# Create objects for each mesh
usd_objects = {}
for data in usd_data:
    blueprint = None
    if (data["name"].startswith("Bl_House_AmerSuburb009_N10")):  # Filter for specific building
        blueprint = blueprints.boxModels[0]
        data["position"] = (6, 0, 2)
    else:
        continue  # Skip non-target meshes
        
    usd_obj = new Prop with shape BoxShape(dimensions=(data["width"], data["length"], data["height"])),
        at data["position"],  # Use extracted position
        facing data["orientation"],  # Use extracted orientation (yaw, pitch, roll)
        with allowCollisions True, with requireVisible False, with regionContainedIn workspace.region, with blueprint blueprint
    usd_objects[data["name"]] = usd_obj

print(usd_objects.keys())

building = usd_objects["Bl_House_AmerSuburb009_N10"]

ego = new Car # left of building by 10