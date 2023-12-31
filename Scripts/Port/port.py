from Scripts.BerthPlanner.berth_planner import BerthPlanner
from Scripts.YardPlanner.yard_planner import YardPlanner
import simpy

class Port:
    def __init__(self, 
                 env:simpy.Environment) -> None:
        self.env:simpy.Environment = env
        self.berth_planner:BerthPlanner = BerthPlanner(env)
        self.yard_planner:YardPlanner = YardPlanner(env) 