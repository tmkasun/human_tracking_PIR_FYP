import numpy as np
from theano import function, grad
from theano import tensor as T
from theano import shared
import matplotlib.pyplot as plt

def plot_line(data):
    c = data[2]
    m = data[0]
    y_coefficient = trained_weights[1]

    x = np.linspace(-10, 10, 50)  # 100 linearly spaced numbers
    y = (m * x + c - 1) / (-y_coefficient)

    # compose plot
    plt.plot(x, y, label='$y = {m}x + {c}$'.format(m=m, c=c))


x = T.dmatrix('x')  # Input matrix

w = T.dvector('w')  # Weight vector

s = T.dot(x, w)

layer_out = function([x, w], s)

training_data = np.array(
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
weight_update_function = function([training_input, weight_delta], weight_update,
                                  updates=[(weight_vector_synapses0, weight_vector_synapses0 + weight_update)])

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