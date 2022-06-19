from network import Network
import numpy as np
nn=Network([4,3,2,1])
print(nn.weights)
print(nn.biases)
z,a=nn.feedForward(np.array([[1,2,3,1],[1,2,3,1]]))
# print(z)
print(list(a[-1].squeeze()))
# print(nn.gradient(a,z))