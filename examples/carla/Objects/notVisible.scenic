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
    usd_obj = new Prop with shape BoxShape(dimensions=(data["width"], data["length"], data["height"])),
        at data["position"],  # Use extracted position
        facing data["orientation"],  # Use extracted orientation (yaw, pitch, roll)
        with allowCollisions True, with requireVisible False, with regionContainedIn workspace.region, with occluding True

    usd_objects[data["name"]] = usd_obj

ego = new Car at (132.9721, -198.746811, 2.572), facing (90, 0, 0)

chair = new Chair not visible from ego, at (92.1711, -227.1949, 2), with regionContainedIn workspace.region