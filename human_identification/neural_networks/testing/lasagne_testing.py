from numpy import dtype

__author__ = 'tmkasun'
import lasagne
import cv2

uniform_dist = lasagne.init.Uniform(range=50, mean=100, std=498)
normal_dist = lasagne.init.Normal(mean=100, std=49)

flir_lepton_sample_n = normal_dist.sample((800, 600)).astype('uint8')
flir_lepton_sample_u = uniform_dist.sample((800, 600)).astype('uint8')

cv2.imshow("Lepton Sample Frame Uniform", flir_lepton_sample_u)
cv2.imshow("Lepton Sample Frame Normal", flir_lepton_sample_n)
cv2.waitKey(0)

