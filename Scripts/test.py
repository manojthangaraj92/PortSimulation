from typing import List, Any, Optional, Dict, Tuple
import simpy
from Scripts.basic_objects import Resource, BasicObject, Event

class Crane(Resource):
    """
    This class represents a crane object. It's simpy resource
    """
    def __init__(self, 
                 name:str, 
                 env:simpy.Environment, 
                 capacity:int=1) -> None:
        super().__init__(env, capacity)
        self.name = name
        self.vessel:Vessel = None

    def action(self):
        if self.vessel is not None:
            pass

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
        self.occupied_by:List[Vessel] = []

class HatchProfile:
    """
    The base class for hatch profiles. It  stores information about the particular hatch
    information in the ship.
    """
    def __init__(self, name:str):
        """
        Constructor for the hatch profiles class

        @param name: name of the hatch profile.
        """
        self.name: str= name
        self.num_rows: int= 0
        self.rows: List[Dict[str:Any]]= []

    def add_row(self, operation_type:str,
                container_type:str,
                container_size:Any, 
                min_value:int, 
                max_value:int) -> None:
        """
        This function create a row of operation about type of operation, 
        related container type and size, the min and max number of containers

        @param operation_type: whether its loading and discharging
        @param container_type: whether its Full or Empty etc.,
        @param container_size: size of the container
        @param min_value: min value that number of containers has to be generated
        @param max_value: max value that number of containers hast to be generated
        """
        row = {
            "operation_type": operation_type,
            "container_type": container_type,
            "container_size": container_size,
            "min_value": min_value,
            "max_value": max_value
        }
        self.rows.append(row)
        self.num_rows += 1

    def __str__(self):
        profile_str = f"Hatch Profile: {self.name}\nNumber of Rows: {self.num_rows}\n"
        for i, row in enumerate(self.rows, start=1):
            profile_str += f"Row {i}: Operation Type: {row['operation_type']}, Container Type: {row['container_type']}, "
            profile_str += f"Container Size: {row['container_size']}, Min Value: {row['min_value']}, Max Value: {row['max_value']}\n"
        return profile_str
    
class Vessel:
    """
    Base class for vessel. The vessel has all the information about its hatch profiles.
    """
    count = 0 #to count the number of Vessel created in the model

    def __init__(self, 
                 env,
                 name:str,
                 length:Optional[float]=300, 
                 width:Optional[float]=30):
        """
        Constructor for the vessel class.

        @param name: name of the ship
        @param length: length of the ship
        @param width: width of the ship
        """
        self.env = env
        self.name:str = name
        self.length:float = length
        self.width:float = width
        self.hatch_profiles:HatchProfile = []  # List to store hatch profiles
        self.berth:Berth = None
        self.berth_request:Berth.request = None
        self.cranes:List[Tuple[Crane, Crane.request]] = []
        Vessel.count += 1
    
    def set_berth(self, 
                  berth:Berth, 
                  berth_request:Berth.request) -> Berth:
        """
        When ship arrives, this method requests the berth and stores it the vessel class.
        """
        self.berth = berth
        self.berth_request = berth_request
        berth.occupied_by.append(self)
        return self.berth
    
    def release_berth(self) -> None:
        if self.berth:
            self.berth.release(self.berth_request)
            self.berth.occupied_by.remove(self)
            self.berth = None
            self.berth_request = None
    
    def add_crane(self, 
                  crane:Crane, 
                  crane_request:Crane.request) -> None:
        self.cranes.append((crane, crane_request))

    def release_cranes(self) -> None:
        for crane, req in self.cranes:
            crane.release(req)
        self.cranes.clear()

    def on_berth_acquired(self,
                          berth:Berth, 
                          berth_request:Berth.request):
        # Callback for when the berth is acquired
        self.set_berth(berth, berth_request)

    def on_crane_acquired(self, 
                          crane:Crane, 
                          crane_request:Crane.request):
        # Callback for when a crane is acquired
        self.add_crane(crane, crane_request)

    def num_load_containers(self)-> tuple:
        """
        This method returns total number containers to load
        """
        total_min = 0
        total_max = 0
        for profile in self.hatch_profiles:
            for row in profile.rows:
                if row["operation_type"] == "Load":
                    num_min, num_max = row["min_value"], row["max_value"]
                    total_min += num_min
                    total_max += num_max
        return (total_min, total_max)

    def num_discharge_containers(self)-> tuple:
        """
        This method returns total number of containers to unload
        """
        total_min = 0
        total_max = 0
        for profile in self.hatch_profiles:
            for row in profile.rows:
                if row["operation_type"] == "Unload":
                    num_min, num_max = row["min_value"], row["max_value"]
                    total_min += num_min
                    total_max += num_max
        return (total_min, total_max)

    def add_hatch_profile(self, hatch_profile: HatchProfile) -> None:
        """
        Method to add a hatch profile to the vessel
        """
        self.hatch_profiles.append(hatch_profile)

    def total_containers_to_load(self)-> str:
        """
        Method to return number of containers to be loaded.
        """
        if len(self.hatch_profiles) > 0:
            min_max_containers = self.num_load_containers()
            return f'The containers to load are between {min_max_containers[0]} and {min_max_containers[1]}.'

    def total_containers_to_discharge(self)-> str:
        """
        Method to return number of containers to be unloaded.
        """
        if len(self.hatch_profiles) > 0:
            min_max_containers = self.num_discharge_containers()
            return f'The containers to discharge are between {min_max_containers[0]} and {min_max_containers[1]}.'

    def __str__(self):
        profile_str = f"Vessel: {self.name}, Length: {self.length}, Width: {self.width}\n"
        if self.hatch_profiles:
            profile_str += "Hatch Profiles:\n"
            for i, profile in enumerate(self.hatch_profiles, start=1):
                profile_str += f"Profile {i}: {profile.name}\n"
        profile_str += f"Num Containers: {len(self.container_list)}"
        return 

class VesselArrival:
    """
    This class handles the vessel arrival process
    """
    def __init__(self):
        """
        Constructor for the vessel Arrival
        """
        self.schedule = []
        self.num_vessels = 0

    def add_schedule(self,
                     vessel:Vessel,
                     arrival_time:float,
                     berth_position:int,
                     cranes:List[Crane],
                     prePcat:Optional[float]=1000.00,
                     postPcat:Optional[float]=1000.00) -> None:
        """
        @param vessel: the Vessel object that is created
        @param arrival_time: The arrival time of the vessel
        @param prePcat: pre inspection time done by the authorities
        @param postPcat: post inspection time by the authorities
        @param berthPosition: ships berthing point at the dock.
        """
        if isinstance(vessel, Vessel):
            schedule_event = {
                "vessel": vessel, 
                "arrival_time": arrival_time,
                "berth_position": berth_position,
                "num_cranes": cranes,
                "pre-pcat": prePcat,
                "post-pcat": postPcat
            }
            self.schedule.append(schedule_event)
            self.num_vessels += 1

    def __str__(self):
        return f"{self.num_vessels} is expected to in this simulation"

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
        self.scheduler:VesselArrival = VesselArrival # List of vessel arrival instances
        self.hatch_profiles:List[HatchProfile] = []  # List of hatch profiles

    def add_berth(self, 
                  name:str, 
                  capacity:int) -> Berth:
        """
        Adds a berth to the berth planner. The berth planner
        can have number of berth available.
        """
        self.berth = Berth(self.env, capacity=capacity)
        return self.berth
    
    def add_crane(self, num_cranes:int) -> List[Crane]:
        """
        Adds a crane to the berth planner. It can have any number of cranes
        """
        if num_cranes > 0:
            self.cranes = [Crane(self.env) for i in range(num_cranes)]
        return self.cranes
    
    def add_hatch_profile(self, hatch_profile:HatchProfile) -> List[HatchProfile]:
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

        @param name: The name of the vessel#
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
            
    def process_arrivals(self) -> None:
        for event in self.scheduler.schedule:
            vessel = event["vessel"]
            arrival_time = event["arrival_time"]
            cranes = event["num_cranes"]

            self.env.process(self.handle_vessel_arrival(vessel, arrival_time, cranes))

    def await_berth_acquisition(self, 
                                vessel:Vessel, 
                                berth_request:Berth.request) -> None:
        yield berth_request
        # Trigger callback when berth is acquired
        vessel.on_berth_acquired(self.berth, berth_request)

    def await_crane_acquisition(self, 
                                vessel:Vessel, 
                                crane:Crane, 
                                crane_request:Crane.request) -> None:
        yield crane_request
        # Trigger callback when crane is acquired
        vessel.on_crane_acquired(crane, crane_request)

    def handle_vessel_arrival(self, 
                              vessel:Vessel, 
                              arrival_time:float, 
                              cranes:List[Crane]) -> None:
        yield self.env.timeout(arrival_time - self.env.now)

        # Request berth asynchronously
        berth_request = self.berth.request()
        self.env.process(self.await_berth_acquisition(vessel, berth_request))

        # Request cranes asynchronously
        for crane_name in cranes:
            crane = next((c for c in self.cranes if c.name == crane_name), None)
            if crane:
                crane_request = crane.request()
                self.env.process(self.await_crane_acquisition(vessel, crane, crane_request))
        else:
            print(f"{vessel.name} failed to acquire a berth at time {self.env.now}")
            # Handle the case where berth acquisition failed
