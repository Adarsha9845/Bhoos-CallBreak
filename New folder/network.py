

import numpy as np

class Network:
    def __init__(self, sizes,initialization="gaussian",value=None):
        """
        sizes=[a,b,c,d]
        This represents a four layer network. 
        a is the dimension of input, 
        b is the dimension of first hidden layer
        c is the dimension of second hidden layer.
        d is the dimension of output layer
        
        The initialization can be 'gaussian', 'random' or 'constant'.
        For constant initialization, we need to supply the value of constant with which the 
        weights and the values are to be initialized.
        """
        self.num_layers = len(sizes)
        self.sizes = sizes
        if initialization=="constant" and value==None:
            raise("Value is necessary for constant initialization!!!")
        if initialization=="gaussian" or initialization=="xavier":
            self.biases = [np.random.randn(1,y) for y in sizes[1:]]
            self.weights = [np.random.randn(y,x)*np.sqrt(1/x) for x,y in zip(sizes[:-1], sizes[1:])]
        elif initialization=="random":
            self.biases = [np.random.rand(1,y) for y in sizes[1:]]
            self.weights = [np.random.rand(y,x)*np.sqrt(1/x) for x,y in zip(sizes[:-1], sizes[1:])]
        elif initialization=="constant":
            self.biases = [np.array([[value] * y])  for y in sizes[1:]]
            self.weights = [np.array([[value] * x ]* y) for x,y in zip(sizes[:-1], sizes[1:])]
        
    def selu(self,z, lambdaa = 1.0506, alpha = 1.6732):
        a = np.where(z >= 0, lambdaa * z, lambdaa * alpha * (np.exp(z) - 1))
        # print("From selu")
        # print(z)
        # print(a)
        # print("from selu")
        return a

    def selu_prime(self,z, lambdaa = 1.0506, alpha = 1.6732):
        return np.where(z >= 0, lambdaa, lambdaa * alpha * np.exp(z))

    def tanh(self,z):
        return np.tanh(z)

    def tanh_prime(self,z):
        return 1-np.square(np.tanh(z))

    def feedForward(self, x):
        activation = x
        activations = [x]
        zs = []
        for b, w in zip(self.biases[:-1], self.weights[:-1]):
            z = np.matmul(activation,w.T) + b
            zs.append(z)
            activation = self.tanh(z)
            activations.append(activation)
        z = np.matmul(activation,self.weights[-1].T) + self.biases[-1]
        zs.append(z)
        activation = self.selu(z)
        activations.append(activation)
        return zs, activations
    
    def gradient(self, activations, zs):
        nabla_b = [np.zeros(np.array(b).shape) for b in self.biases]
        nabla_w = [np.zeros(np.array(w).shape) for w in self.weights]
        nabla_b[-1] = np.sum(self.selu_prime(zs[-1]),axis=0,keepdims=True)
        # print("From function gradient:::")
        # print(zs[-1].shape)
        # print(activations[-2].shape)
        delta=self.selu_prime(zs[-1])
        nabla_w[-1] = np.matmul(delta.T ,activations[-2])
        
        for layer in range (2, self.num_layers):

            delta=np.matmul(delta,self.weights[-layer+1])
            z = zs[-layer]
            sp = self.tanh_prime(z)
            
            delta = delta* sp
            nabla_b[-layer] = np.sum(delta,axis=0,keepdims=True)
            
            nabla_w[-layer] = np.matmul(delta.T, activations[-layer - 1])
            
        return nabla_b, nabla_w
    
    
    def batch_normalization():
        pass



            
         


            
            
        
        
        
        











