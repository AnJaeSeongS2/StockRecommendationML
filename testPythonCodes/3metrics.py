import tensorflow as tf
import numpy as np

# make 100 phony data points in NumPy.
x_data = np.float32(np.random.rand(2,100))
y_data = np.dot([0.100,0.200], x_data)+ 0.300

#Construct a linear model.
b= tf.Variable(tf.zeros([1]))
W = tf.Variable(tf.random_uniform([1,2],-1.0, 1.0))
y = tf.matmul(W, x_data) +b

#Minimize the squared errors.
loss = tf.reduce_mean(tf.square(y - y_data))
optimizer = tf.train.GradientDescentOptimizer(0.5)
train = optimizer.minimize(loss)

#for initializing the variables
init = tf.initialize_all_variables()

#launch the graph
sess = tf.Session()
sess.run(init)

#fit the plane.
for step in xrange(0, 2001):
	sess.run(train)
	if step%20 == 0:
		print step, sess.run(W), sess.run(b)

# learns best fit is W: [[0.100 0.2000]], b: [0.300]
