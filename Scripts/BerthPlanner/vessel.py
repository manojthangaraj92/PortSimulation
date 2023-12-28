from Scripts.Resources.resources import *

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
                 env:simpy.Environment,
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
        self.hatch_profiles:List[HatchProfile] = []  # List to store hatch profiles
        self.finished_hatches:int = 0
        self.finished_hatch_profiles:List[HatchProfile] = []
        self.berth:Berth = None
        self.berth_request:Berth.request = None
        self.cranes:List[Tuple[Crane, Crane.request]] = []
        self._prePcat:int = 0
        self._postPcat:int = 0
        self._arrivalTime:int = 0
        Vessel.count += 1
    
    @property
    def prePcat(self) -> float:
        return self._prePcat
    
    @prePcat.setter
    def prePcat(self,
                time:float) -> None:
        if not isinstance(time, float):
            raise ValueError("prePcat must be an integer")
        self._prePcat = time
    
    @property
    def postPcat(self) -> float:
        return self._postPcat
    
    @postPcat.setter
    def postPcat(self,
                time:float) -> None:
        if not isinstance(time, float):
            raise ValueError("postPcat must be an integer")
        self._postPcat = time

    @property
    def arrivalTime(self) -> float:
        return self._arrivalTime
    
    @arrivalTime.setter
    def arrivalTime(self,
                time:float) -> None:
        if not isinstance(time, float):
            raise ValueError("arrivalTime must be an integer")
        self._arrivalTime = time

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
        if self.berth and not self.cranes:
            print(f"The {self.name} starts the post_pcat inspection at {self.env.now}")
            yield self.env.timeout(self.postPcat)
            print(f"The {self.name} finished the post_pcat inspection at {self.env.now}")
            self.berth.release(self.berth_request)
            self.berth.occupied_by.remove(self)
            print(f"{self.berth.name} has completed all tasks for {self.name} at {self.env.now}")
            self.berth = None
            self.berth_request = None
    
    def add_crane(self, 
                  crane:Crane, 
                  crane_request:Crane.request) -> None:
        self.cranes.append((crane, crane_request))
        crane.vessel = self

    def release_cranes(self, 
                       crane:Crane) -> None:
        for crane_in_vessel, req in self.cranes:
            if crane_in_vessel.name == crane.name:
                crane.release(req)
                crane.vessel = None
                self.cranes.remove((crane,req))

        if not self.cranes:
            self.env.process(self.release_berth())

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

    def start_crane_operations(self,
                               crane:Crane) -> None:
        self.env.process(crane.process_hatch_profiles(self))

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
        return profile_str
    
class VesselArrival:
    """
    This class handles the vessel arrival process
    """
    def __init__(self,env:simpy.Environment):
        """
        Constructor for the vessel Arrival
        """
        self.env = env
        self.schedule:List[Dict] = []
        self.num_vessels:int = 0

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
                "cranes": cranes,
                "pre-pcat": prePcat,
                "post-pcat": postPcat
            }
            self.schedule.append(schedule_event)
            self.num_vessels += 1

    def __str__(self):
        return f"{self.num_vessels} is expected to in this simulation"