__author__ = 'tmkasun'

from theano.tensor.shared_randomstreams import RandomStreams
from theano import function, pp

seed = 200
rnd_dist = RandomStreams(seed=seed)

uni_dist = rnd_dist.uniform((1, 10), low=5, high=100)

draw_random_samples = function([], uni_dist)

print(draw_random_samples())