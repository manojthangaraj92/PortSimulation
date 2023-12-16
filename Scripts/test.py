from Scripts.vessel import Vessel
import simpy

env = simpy.Environment()

vessel = Vessel(env,
                "test")
vessel.postPcat = 1000
vessel.prePcat = 2000

print(vessel.prePcat)