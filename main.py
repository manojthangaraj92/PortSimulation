from Scripts import *
import simpy
import datetime

#define the global variables
RANDOM_SEED = 42
SIMULATION_TIME = 1000000

log_path = f'./log_files/{datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")}.log'
log_file = Logger(log_path)

# Create a SimPy environment
env = simpy.Environment()

# Create a BerthPlanner instance
yard_planner = YardPlanner(env)
berth_planner = BerthPlanner(env, yard_planner, log_file)

# Create berth and crane and add it to the berth planner instance
berth1 = berth_planner.add_berth("Berth1",capacity=2)
crane1 = berth_planner.add_crane("Crane1")
crane2 = berth_planner.add_crane("Crane2")

# Add the hatch profiles
hatch_profile = HatchProfile("Hatch_1")
hatch_profile.add_row(ContainerHandling.DISCHARGE, ContainerType.LADEN, ContainerSize.TWENTY_FT, 100, 120)
hatch_profile.add_row(ContainerHandling.LOAD, ContainerType.LADEN, ContainerSize.FORTY_FT, 200, 220)
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

# Set the yard planner
yard_planner.add_block(1000, "Block1")
yard_planner.add_block(1000, "Block2")

block1 = yard_planner.blocks.add_block(env, 1000, "Block1")
block1.num_bays = 50
block1.num_cells = 6
block1.num_tiers = 6

block2 = yard_planner.blocks.add_block(env, 1000, "Block2")
block2.num_bays = 50
block2.num_cells = 6
block2.num_tiers = 6

berth_planner.process_arrivals()
env.run(until=SIMULATION_TIME)