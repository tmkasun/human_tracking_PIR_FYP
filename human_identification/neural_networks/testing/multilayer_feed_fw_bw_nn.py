import numpy as np
from theano import function, grad
from theano.scalar import float32
from theano import tensor as T

# v = T.scalar('x', float32)
# s = 1 / (1 + T.exp(-v))
# s_d = grad(s, v)
# logit = function([v], s)
# logit_d = function([v], s_d)

np.random.seed(1)

x = T.dmatrix('x')  # Input matrix

w = T.dvector('w')  # Weight vector

s = T.dot(w.T, x)

l0_output = function([x, w], s)

training_data = np.array(
    [
        [0, 0, 1],
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]
)
output_labels = np.array(
    [
        [0, 0, 1, 1]
    ]
)

weight_vector_synapses0 = 2 * np.random.random(3) - 1

print(np.dot(weight_vector_synapses0.T,training_data))

# for iteration in xrange(1000):
# # Do traning
#
# pass