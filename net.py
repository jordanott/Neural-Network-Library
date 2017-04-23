from layer_activations import *
from conv_layer import conv_layer
from input_layer import input_layer
from output_layer import output_layer
from max_pool_layer import max_pool_layer
from fully_connected_layer import fully_connected_layer

import numpy as np

class net():
	def __init__(self,learning_rate=.001):
		self.learning_rate = learning_rate
		self.layers = []
		# layer types
		self.layer_types = {
		'conv':conv_layer,
		'fc':fully_connected_layer,
		'input':input_layer,
		'max_pool':max_pool_layer,
		'output':output_layer
		}
		self.counter = 0

	def add_layer(self,layer_type,shape=0,pool_size=2,stride=1,num_neurons=0,filter_dim=3,num_filters=1,padding=1,activation='relu',output_function='softmax'):
		# layer options
		layer_opts = {
		'stride':stride,
		'padding':padding,
		'pool_size':pool_size,
		'incoming_shape':shape,
		'filter_dim':filter_dim,
		'num_neurons':num_neurons,
		'num_filters':num_filters,
		'output_function':output_function,
		'learning_rate':self.learning_rate		
		}
		# set layer activation function
		layer_opts['activation'] = activation_functions[activation][0]
		layer_opts['backtivation'] = activation_functions[activation][1]

		if self.layers:
			# set depth of filter based off depth of incoming shape
			layer_opts['incoming_shape'] = self.layers[-1].output_shape
		#print layer_type,"********* Incoming shape:",layer_opts['incoming_shape']
		# add new layer
		self.layers.append(self.layer_types[layer_type](layer_opts))
		#print layer_type,"********* Outgoing shape:",self.layers[-1].output_shape


	def forward(self,data):
		l2 = 0
		for layer in self.layers:
			data,reg = layer.forward(data)
			l2 += reg
		return data,l2

	def backward(self,gradient):
		for layer in reversed(self.layers):
			gradient = layer.backprop(gradient)
