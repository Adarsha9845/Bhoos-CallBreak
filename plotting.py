import numpy as np
import matplotlib.pyplot as plt

a=np.linspace(0,2*np.pi,100)
b=np.sin(a)
c=np.cos(a)

# ax1=plt.subplot(2,1,1)
# ax2=plt.subplot(2,1,2)
# ax1.plot(a,b)
# ax1.set_xlabel("Angle in radians(x)")
# ax1.set_ylabel("sin(x)")
# ax1.title.set_text("Sine Wave")

# ax2.plot(a,c)
# ax2.set_xlabel("Angle in radians(x)")
# ax2.set_ylabel("cos(x)")
# ax2.title.set_text("Cos Wave")

# plt.show()

# plt.plot(a,b)
# plt.plot(a,c)
# plt.title("Sine and Cosine curves")
# plt.xlabel("Radians")
# plt.legend(["sine wave","cos wave"])
# plt.show()


plt.figure(figsize=(10,12))
legend=[]
for i in range(4):
    plt.plot(b+i)
    #this prints the player name, epsilon, alpha and gamma of the players
    legend.append(f"sine+{i}")
plt.legend(legend)
plt.title("Expected Rewards")    
plt.show()
        