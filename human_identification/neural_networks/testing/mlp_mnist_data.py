from theano.tensor.shared_randomstreams import RandomStreams

__author__ = 'tmkasun'
import pickle
import numpy as np
import cv2
import theano
import theano.tensor as T


def mnist_summary():
    print("Shapes:")
    print(training_input.shape)
    print(training_label.shape)
    print(validation_input.shape)
    print(validation_label.shape)
    print(testing_input.shape)
    print(testing_label.shape)

    print("Sample training Label:")
    print(training_label[0])

    print("Sample input:")

    sample_image = []
    for index in range(28):
        a = training_input[0][index * 28:index * 28 + 28]
        sample_image.append(a)

    sample_image = np.array(sample_image)

    cv2.imshow("Sample Image", sample_image)
    cv2.waitKey(0)
    assert False


random_streams = T.shared_randomstreams.RandomStreams(seed=1)


def create_weight_matrix(layer_in_neurons, layer_out_neurons):
    random_streams = T.shared_randomstreams.RandomStreams(seed=1)
    weight_function = theano.function([], random_streams.normal((layer_in_neurons, layer_out_neurons)))
    return weight_function()


mnist_pkl = open('data/mnist.pkl', 'r')

(training_input, training_label), (validation_input, validation_label), (testing_input, testing_label) = pickle.load(
    mnist_pkl)

# nist_summary()

input_x = T.matrix('input_x')
correct_labels = T.ivector('correct_labels')

no_hidden_neurons = 500

init_hidden_w = theano.shared(create_weight_matrix(28 * 28, no_hidden_neurons), name='hidden_w')
init_hidden_b = theano.shared(np.zeros(shape=(no_hidden_neurons,)), name='hidden_b')

no_output_neurons = 10  # 10 for each 10 digits 0,1,2,.....,8,9

init_out_w = theano.shared(create_weight_matrix(no_hidden_neurons, no_output_neurons), name='out_w')
init_out_b = theano.shared(np.zeros(shape=(no_output_neurons,)), name='out_b')

hidden_activation = T.tanh(T.dot(input_x, init_hidden_w) + init_hidden_b)

# Breakdown function
hidden_activation_f = theano.function([input_x], hidden_activation)

network_output = T.nnet.softmax(T.dot(hidden_activation, init_out_w) + init_out_b)

# Breakdown function
network_output_f = theano.function([hidden_activation], network_output)

y_estimation = T.argmax(network_output, axis=1)

# Breakdown function
y_estimation_f = theano.function([network_output], y_estimation)

log_likelihood = T.log(network_output)[T.arange(correct_labels.shape[0]), correct_labels]

# Breakdown function
log_likelihood_f = theano.function([network_output,correct_labels], log_likelihood,allow_input_downcast=True)


# We use mean instead of sum to be less dependent on batch size (better for flexibility)
cost = -T.mean(log_likelihood)

# Breakdown function
cost_f = theano.function([log_likelihood],cost)

parameters = [init_hidden_w, init_hidden_b, init_out_w, init_out_b]
gradients = T.grad(cost, parameters)

learning_rate = 0.01

train_update = [(param, param - learning_rate * gradient) for param, gradient in zip(parameters, gradients)]

f_train = theano.function([input_x, correct_labels], cost, updates=train_update, allow_input_downcast=True)
f_test = theano.function([input_x], y_estimation, allow_input_downcast=True)

batch_size = 100
epochs = 10

training_batches = len(training_input) / batch_size
testing_batches = len(testing_input) / batch_size
validation_batches = len(validation_input) / batch_size

for epoch in range(epochs):

    print("Epoch {}:".format(epoch + 1))
    train_cost = []
    train_accuracy = []

    for batch in range(training_batches):
        start_position = batch * batch_size
        end_position = start_position + batch_size

        batch_inputs = training_input[start_position:end_position]
        batch_labels = training_label[start_position:end_position]

        batch_cost = f_train(batch_inputs, batch_labels)
        # # Steps breakdown
        # act_sig = hidden_activation_f(batch_inputs)
        # # print("Activation signal")
        # # print(act_sig)
        # net_out = network_output_f(act_sig)
        # # print("Network Output")
        # # print(net_out)
        # y_est = y_estimation_f(net_out)
        # print("Output Estimation")
        # print(y_est)
        # log_like = log_likelihood_f(net_out,batch_labels)
        #
        # print("log_likelog_like")
        # print(log_like)
        #
        # cost_t = cost_f(log_like)
        # print("Cost")
        # print(cost_t)

        batch_predict = f_test(batch_inputs)

        accuracy = sum(batch_predict == batch_labels) / float(batch_size)

        train_cost.append(batch_cost)
        train_accuracy.append(accuracy)

    print("Cost% : {}, Accuracy%: {}".format(np.mean(train_cost),
                                             100 * np.mean(train_accuracy)))