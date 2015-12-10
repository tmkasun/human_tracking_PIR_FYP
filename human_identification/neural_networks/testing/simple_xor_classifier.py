# coding=utf-8
import numpy as np
from theano import function, grad
from theano import tensor as T
from theano import shared
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_hyper_plane():
    point  = np.array([1, 2, 3])
    normal = np.array([1, 1, 2])

    # a plane is a*x+b*y+c*z+d=0
    # [a,b,c] is the normal. Thus, we have to calculate
    # d and we're set
    d = -point.dot(normal)

    # create x,y
    xx, yy = np.meshgrid(range(10), range(10))

    # calculate corresponding z
    z = (-normal[0] * xx - normal[1] * yy - d) * 1. /normal[2]

    # plot the surface
    plt3d = plt.figure().gca(projection='3d')
    plt3d.plot_surface(xx, yy, z)
    plt.show()
    assert False

def plot_line(data):
    c = data[2]
    m = data[0]
    y_coefficient = trained_weights[1]

    x = np.linspace(-10, 10, 50)  # 100 linearly spaced numbers
    y = (m * x + c - 1) / (-y_coefficient)

    # compose plot
    plt.plot(x, y, label='$y = {m}x + {c}$'.format(m=m, c=c))

# plot_hyper_plane() #TODO Isn't this learning is a hyperplane ?

x = T.dmatrix('x')  # Input matrix

w = T.dvector('w')  # Weight vector

s = T.dot(x, w)

layer_out = function([x, w], s)

training_data = np.array(  # (4,3) The first dimension of a tensor is usually the batch dimension, follow…
    [
        [0, 0, 1],
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 1]
    ]
)
output_labels = np.array(

    [0, 0, 1, 1]

).T

np.random.seed(1)
weight_vector_synapses0 = 2 * np.random.random(3) - 1
weight_vector_synapses0 = shared(weight_vector_synapses0, name='l0_weight_vector')

error = T.dvector('error')
weight_gradient = T.dvector('weight_gradient')

v = T.dvector('v')
s = 1 / (1 + T.exp(-v))
s_d = s * (1 - s)
logit = function([v], s)
logit_d = function([v], s_d)

weight_delta = T.dvector('w_d')
training_input = T.dmatrix('t_in')
weight_update = T.dot(weight_delta, training_input)
learning_rate = 0.2
weight_update_function = function([training_input, weight_delta], weight_update,
                                  updates=[(weight_vector_synapses0,
                                            weight_vector_synapses0 + weight_update * learning_rate)])  # Gradient decent approach

delta_update = function([error, weight_gradient], error * weight_gradient)

for iteration in xrange(1000):
    l0_output = layer_out(training_data, weight_vector_synapses0.get_value())
    activation_signal = logit(l0_output)
    l1_error = output_labels - activation_signal

    l1_delta = delta_update(l1_error, logit_d(activation_signal))

    weight_update_function(training_data, l1_delta)

    if (iteration % 250 == 0) and (iteration != 0):
        trained_weights = weight_vector_synapses0.get_value()
        plot_line(trained_weights)

print(activation_signal)
trained_weights = weight_vector_synapses0.get_value()
plot_line(trained_weights)

x = [0, 1, 1, 0]
y = [0, 1, 0, 1]
plt.scatter(x, y)
plt.legend(loc='best')
plt.show()  # show the plot