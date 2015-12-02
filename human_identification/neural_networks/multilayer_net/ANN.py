__author__ = 'akila'

import numpy as np
import dataset as data

input_set = data.X
output_set = data.Y
norm_set = np.zeros(shape=np.shape(input_set))

# logistic function

def sigmoid(x, deriv=False):
    if (deriv == True):
        return x * (1 - x)
    return 1 / (1 + np.exp(-x))


def mean_var_calc():

    mean = input_set.mean()
    var = input_set.var()

    for n in range(len(input_set)):
        for p in range(len(input_set[0])):
            x = input_set[n][p]
            norm_set[n][p] = (x-mean) / var
            print norm_set[n][p]

    # for x in np.nditer(input_set):
    #
    #     x = (x-mean) / var
    #     norm_set[i]= x
    #     print norm_set[i]
    #     print '--------------'


def write_array():
    for x in np.nditer(norm_set):
        print x

np.random.seed(1)

# randomly initialize weights vectors with mean 0

weight_vec0 = 2 * np.random.random((3, 4)) - 1
weight_vec1 = 2 * np.random.random((4, 1)) - 1

mean_var_calc()
#write_array()

for j in xrange(60000):

    # Feed forward through layers 0, 1, and 2

    l0 = norm_set
    l1 = sigmoid(np.dot(l0, weight_vec0))
    l2 = sigmoid(np.dot(l1, weight_vec1))

    # calculate the error for hidden layer 1
    l2_error = output_set - l2

    # Track the error
    if (j % 10000) == 0:
        print "Error:" + str(np.mean(np.abs(l2_error)))

    # Calculate the learning rate for hidden layer 1
    l2_delta = l2_error * sigmoid(l2, deriv=True)

    # calculate the error for hidden layer 1
    l1_error = l2_delta.dot(weight_vec1.T)

    # Calculate the learning rate for input layer
    l1_delta = l1_error * sigmoid(l1, deriv=True)

    # Update weight vectors with learning rate
    weight_vec1 += l1.T.dot(l2_delta)
    weight_vec0 += l0.T.dot(l1_delta)

print l2