from typing import List, Any, Optional, Dict, Tuple
import simpy
from Scripts.Resources.resources import Berth, Crane
from Scripts.BerthPlanner.vessel import Vessel, VesselArrival, HatchProfile

class BerthPlanner:
    """
    The Berth planner is a entity that holds the berth, crane, vessels details. It holds all the informations
    needed for executing berth operations.
    """
    def __init__(self, env:simpy.Environment):
        self.env = env
        self.berth:Berth = None  # List of available berths
        self.cranes:List[Crane] = []  # List of crane instances
        self.vessels: List[Vessel] = [] # List of Vessels instances
        self.scheduler:VesselArrival = VesselArrival(env) # List of vessel arrival instances
        self.hatch_profiles:List[HatchProfile] = []  # List of hatch profiles

    def add_berth(self, 
                  name:str, 
                  capacity:int) -> Berth:
        """
        Adds a berth to the berth planner. The berth planner
        can have number of berth available.
        """
        self.berth = Berth(name, self.env, capacity=capacity)
        return self.berth
    
    def add_crane(self, 
                  name:str) -> List[Crane]:
        """
        Adds a crane to the berth planner. It can have any number of cranes
        """
        self.cranes.append(Crane(name, self.env, capacity=1))
        return self.cranes
    
    def add_hatch_profile(self, 
                          hatch_profile:HatchProfile) -> List[HatchProfile]:
        """
        This method adds the hatch profile to the berth planner

        @param hatch_profile: The hatch profile instace to add
        """
        if isinstance(hatch_profile, HatchProfile):
            self.hatch_profiles.append(hatch_profile)
        return self.hatch_profiles
    
    def add_vessel(self,
                   name:str,
                   length:Optional[float]=300, 
                   width:Optional[float]=30) -> Vessel:
        """
        This method adds the vessel to the berth planner

        @param name: The name of the vessel
        @param length: Then length of the vessel in meters
        @param width: The width of the vessel in meters

        return: the vessel object
        """
        vessel = Vessel(self.env,
                        name,
                        length,
                        width)
        self.vessels.append(vessel)
        return vessel

    def add_to_schedule(self,
                        vessel:Vessel,
                        arrival_time:float,
                        berth_position:int,
                        cranes:List[Crane],
                        prePcat:Optional[float]=1000.00,
                        postPcat:Optional[float]=1000.00)->None:
        """
        Function to add the ship arrival scheduler to the schedule

        @param vessel: vessel object 
        @param arrival_time: The arrival time of the vessel
        @berth_position: The position of the berth where the ship will be docked
        @num_cranes: The cranes needed to operate in the ship
        @prePcat: The pre inspection time done by authorities on the ship
        @postPcat: The post inspection time done by the port aunthorities on this ship

        returns None
        """
        if (isinstance(vessel, Vessel) and vessel in self.vessels):
            self.scheduler.add_schedule(vessel,
                                        arrival_time,
                                        berth_position,
                                        cranes,
                                        prePcat,
                                        postPcat)
    def await_berth_acquisition(self, 
                                vessel:Vessel,
                                cranes:List[Crane]) -> None:
        berth_request = self.berth.request()
        yield berth_request
        if (berth_request in self.berth.users):
            print(f'The {vessel.name} started the pre-inspection at {self.env.now}')
            yield self.env.timeout(vessel.prePcat)
            print(f'The {vessel.name} finished the pre-inspection at {self.env.now}')
            print(f'The {vessel.name} is started the operation at {self.env.now}')
            vessel.on_berth_acquired(self.berth, berth_request)
            for crane_name in cranes:
                crane = next((c for c in self.cranes if c.name == crane_name.name), None)
                if crane:
                    self.env.process(self.await_crane_acquisition(vessel, crane))

    def await_crane_acquisition(self, 
                                vessel:Vessel, 
                                crane:Crane) -> None:
        crane_request = crane.request()
        yield crane_request
        if (crane_request in crane.users):
            vessel.start_crane_operations(crane)
            vessel.on_crane_acquired(crane, crane_request)

    def handle_vessel_arrival(self, 
                              vessel:Vessel, 
                              arrival_time:float,
                              cranes:List[Crane]) -> None:
        yield self.env.timeout(arrival_time - self.env.now)
        print(f'The {vessel.name} is arrived at {self.env.now}')
        self.env.process(self.await_berth_acquisition(vessel, cranes))

    def process_arrivals(self) -> None:
        for event in self.scheduler.schedule:
            vessel = event["vessel"]
            arrival_time = event["arrival_time"]
            cranes = event["cranes"]
            vessel.prePcat = event["pre-pcat"]
            vessel.postPcat = event["post-pcat"]
            vessel.arrivalTime = event["arrival_time"]
            self.env.process(self.handle_vessel_arrival(vessel, arrival_time, cranes))