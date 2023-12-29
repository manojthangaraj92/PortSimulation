from Scripts.YardPlanner import Block
import simpy
env = simpy.Environment()
x = Block(env, 1, "x")
print(x.name)