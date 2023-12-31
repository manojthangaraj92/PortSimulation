from typing import List, Any, Optional, Dict, Tuple
import simpy
from Scripts.Utils.basic_objects import Resource
from Scripts.Utils.port_objects_definition import *
from Scripts.YardPlanner.yard_planner import *
import random

class Berth(Resource):
    """
    This class represents the berth and its capacity to accomodate vessels.
    This is simpy resource
    """
    def __init__(self, name:str,
                 env:simpy.Environment, 
                 capacity:int) -> None:
        super().__init__(env, capacity)
        self.name = name
        self.occupied_by:List[Any] = []

    def __str__(self):
        return f"This berth object name is {self.name}"
    
class Crane(Resource):
    """
    This class represents a crane object. It's simpy resource
    """
    def __init__(self, 
                 name:str, 
                 env:simpy.Environment,
                 yard_planner:YardPlanner,
                 capacity:int=1) -> None:
        super().__init__(env, capacity)
        self.env = env
        self.name = name
        self.vessel:Any = None
        self.truck_gang:Any = None
        self.yard_planner = yard_planner

    def process_hatch_profiles(self, 
                               vessel:Any) -> None:
        self.vessel = vessel
        if len(vessel.hatch_profiles)>0:
            for _ in vessel.hatch_profiles:
                # Assuming hatch is a tuple (min_containers, max_containers)
                hatch = vessel.hatch_profiles.pop()
                for row in hatch.rows:
                    min_containers, max_containers = row["min_value"], row["max_value"]
                    num_containers = random.randint(min_containers, max_containers)

                    if row["operation_type"] == ContainerHandling.DISCHARGE:
                        container_type = row["container_type"]
                        container_size = row["container_size"]
                        for _ in range(num_containers):
                            container_created = self.yard_planner.container_factory.create_container(
                                container_type,
                                container_size
                            )
                            container_created.from_interface = CTInterface.VESSEL_INTERFACE
                            container_created.to_interface = CTInterface.YARD_INTERFACE
                            yield self.env.timeout(1200)  # 100 seconds for each container
                            print(f"{self.name} moved a container from {vessel.name} at {self.env.now}")
                            block, bay, cell = self.yard_planner.container_placement_rule.find_placement_by_bay(
                                self.yard_planner.block_list, 
                                container_created
                                )
                            self.yard_planner.yard_place_container(
                                container_created, 
                                block, 
                                bay, 
                                cell
                                )
                    elif row["operation_type"] == ContainerHandling.LOAD:
                        for _ in range(num_containers):
                            yield self.env.timeout(100)  # 100 seconds for each container
                            print(f"{self.name} moved a container from {vessel.name} at {self.env.now}")

                vessel.finished_hatches += 1
                vessel.finished_hatch_profiles.append(hatch)
        print(f"{self.name} has completed all tasks for {vessel.name} at {self.env.now}")
        vessel.release_cranes(self)

    def move_containers(self,
                        yard_planner:YardPlanner,
                        vessel:Any) -> None:
        pass
        
    def __str__(self):
        return f"This Crane Object name is {self.name}"