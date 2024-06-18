import numpy as np
from sys import path as sys_path
sys_path.append('../')
import hiperwalk as hpw

num_vert = 41
line = hpw.Line(num_vert)
qw = hpw.Coined(line)

num_steps = num_vert // 2
center = num_vert // 2
entries = [[1, (center, center + 1)],
           [-1j, (center, center - 1)]]
init_state = qw.state(entries)
print(init_state)

states = qw.simulate((num_steps + 1), init_state)
print(states)
probs = qw.probability_distribution(states)
print(probs.sum(axis=1))
# print('---------------------------------------------------')
# states = qw.simulate((num_steps + 1), init_state)
# print(states)
