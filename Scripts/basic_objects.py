from typing import Union
import simpy
from simpy.core import Environment

class Resource(simpy.Resource):
    """
    Base Class of Simpy Resource
    """
    def __init__(self, env:simpy.Environment, capacity:int):
        super().__init__(env = env, capacity = capacity) 

    def execute_task(self, task_name):
        print(f"Executing task: {task_name} at time {self.env.now:.2f}")
        # Add task execution logic here

class PriorityResource(simpy.PriorityResource):
    """
    Base class for priority rersource
    """
    def __init__(self, env:simpy.Environment, capacity:int):
        super().__init__(env=env, capacity=capacity)

class PreemptiveResource(simpy.PreemptiveResource):
    """
    Base class for priority rersource
    """
    def __init__(self, env:simpy.Environment, capacity:int):
        super().__init__(env=env, capacity=capacity)

class Container(simpy.Container):
    """
    Base Class for Simpy Containers
    """
    def __init__(self, env:simpy.Environment, capacity:int):
        super().__init__(env, capacity=capacity)

class Stores(simpy.Store):
    """
    Base class for Simpy Stores
    """
    def __init__(self, env:simpy.Environment, capacity:int):
        super().__init__(env, capacity=capacity)

class FilterStore(simpy.FilterStore):
    """
    Base class for Filter store resource type
    """
    def __init__(self, env: Environment, capacity: float | int = ...):
        super().__init__(env, capacity)

class EventHandler:
    def __init__(self, env:simpy.Environment):
        self.env = env
        self.processes = []

    def add_process(self, process:simpy.Process):
        """ Adds a process to the list of processes to be handled. """
        self.processes.append(process)

    def run(self):
        """ Runs all processes added to the EventHandler. """
        for process in self.processes:
            self.env.process(process)
