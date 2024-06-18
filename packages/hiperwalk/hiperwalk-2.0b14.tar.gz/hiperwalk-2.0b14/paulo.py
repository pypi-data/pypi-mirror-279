import hiperwalk as hpw
import numpy as np
import scipy.sparse as ss
# import neblina

HPC = 'cpu'
hpw.set_hpc(HPC)

num_vert = 41
line = hpw.Line(num_vert)
qw = hpw.Coined(line)

num_steps = num_vert // 2
center = num_vert // 2
entries = [[1, (center, center + 1)],
           [-1j, (center, center - 1)]]
init_state = qw.state(entries)

################# with hpc ##############
hpc_states = qw.simulate((num_steps + 1), init_state)
probs = qw.probability_distribution(hpc_states)
print(probs.sum(axis=1))

################# with no hpc ##############
hpw.set_hpc(None)
states = qw.simulate((num_steps + 1), init_state)
probs = qw.probability_distribution(states)
probs = probs.sum(axis=1)
print(probs)
print(np.ones(probs.shape))
print(np.allclose(probs, np.ones(probs.shape)))
print('comparing all intermediate states')
diff = states - hpc_states
print(diff.min())
print(diff.max())
print(np.allclose(states, hpc_states))
print(np.allclose(states, hpc_states, rtol=1e-15, atol=1e-15))
