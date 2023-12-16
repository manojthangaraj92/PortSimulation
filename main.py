from Scripts.berth_planner import *
from Scripts.basic_objects import EventHandler
import simpy

#define the global variables
RANDOM_SEED = 42
SIMULATION_TIME = 10000

# Create a SimPy environment
env = simpy.Environment()

#event handler instance
event_handler = EventHandler(env)

# Create a BerthPlanner instance
berth_planner = BerthPlanner(env)

# Create berth and crane and add it to the berth planner instance
berth1 = berth_planner.add_berth("Berth1",capacity=2)
crane1 = berth_planner.add_crane("Crane1")
crane2 = berth_planner.add_crane("Crane2")

# Add the hatch profiles
hatch_profile = HatchProfile("Hatch_1")
hatch_profile.add_row("Load", "Standard", "20ft", 5, 5)
hatch_profile.add_row("Unload", "Reefer", "40ft", 8, 8)
hatch_profile1 = hatch_profile

vessel_1 = berth_planner.add_vessel("Vessel1")
vessel_1.add_hatch_profile(hatch_profile)
vessel_1.add_hatch_profile(hatch_profile1)
berth_planner.add_hatch_profile(hatch_profile)
#print(vessel_1.total_containers_to_discharge(), vessel_1.total_containers_to_load())

vessel_2 = berth_planner.add_vessel("Vessel2")
vessel_2.add_hatch_profile(hatch_profile)
vessel_2.add_hatch_profile(hatch_profile1)
berth_planner.add_hatch_profile(hatch_profile)

berth_planner.add_to_schedule(vessel=vessel_1,
                              arrival_time=10.0,
                              berth_position=1,
                              cranes = berth_planner.cranes)

berth_planner.add_to_schedule(vessel=vessel_2,
                              arrival_time=20.0,
                              berth_position=1,
                              cranes = berth_planner.cranes)

berth_planner.process_arrivals()
env.run(until=SIMULATION_TIME)