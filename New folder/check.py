from gameMaster import GameMaster
from cards import Cards

# played=['4C', 'TC', 'KC', '6C']
# spades=[]
# firstSuit=[]
# for card in played:
#     if card[1]=="S":
#         spades.append(card)
#     elif card[1]==played[0][1]:
#         firstSuit.append(card)
# winner=0
# if len(spades)!=0:
#     winner=spades[0]
#     for card in spades[1:]:
#         if Cards.getRank(card)["value"]>Cards.getRank(winner)["value"]:
#             winner=card
# elif len(firstSuit)>=1:
#     winner = firstSuit[0]
#     for card in firstSuit[1:]:
#         if Cards.getRank(card)["value"]>Cards.getRank(winner)["value"]:
#             winner=card
# print(played.index(winner))

# GameMaster.playInfo['played']=['KD', '3D', '5S']
# GameMaster.playInfo['cards']=['2S', '5C', '4H']
# print(GameMaster.checkCompatibility('9C'))

# cards=[['1D', '7C', '9C', 'TH', '8D', '9D', '8S', '9S', '6H', '5C', '1S', '2S', '7S'],\
# ['2D', '6S', 'QH', '7D', '3S', '4D', '8C', '5D', 'KD', '8H', 'KC', 'JC', '4S'],\
# ['4C', '6C', '5H', '9H', 'JD', 'JS', '2C', 'KS', 'QC', '5S', 'TS', 'KH', '4H'],\
# ['JH', 'QS', '2H', '3H', '1C', 'TD', '3C', 'TC', '1H', '7H', '6D', '3D', 'QD']]
# print(GameMaster.checkCards(cards))
import numpy as np
 
a=[np.array([[1,2,3],[0,0,0]]),np.array([[1,2,-3],[33,4,5]])]
b=[np.array([[22,33,44]]),np.array([[2,3,4]])]
 
with open("weights.nt","w") as outfile:
    # writing the length of weights and biases
    outfile.write(str(len(a))+"\n")
    outfile.write(str(len(b))+"\n")

    # starting of the weights 
    # writing the size of the weight
    for weight in a:
        # writing the number of dimensions of the array
        outfile.write(str(len(weight.shape))+"\n")
        # writing the value of each dimension into the file
        for dim in weight.shape:
            outfile.write(str(dim)+"\n")
        #now writing the values of the arrays
        for el in weight.flatten():
            outfile.write(str(el)+"\n")

    # starting of the biases 
    # writing the size of the biases
    for bias in b:
        # writing the number of dimensions of the array
        outfile.write(str(len(bias.shape))+"\n")
        # writing the size of dimensions into the file
        for dim in bias.shape:
            outfile.write(str(dim)+"\n")
        #now writing the values of the arrays
        for el in bias.flatten():
            outfile.write(str(el)+"\n")

        
            
    

with open("weights.nt" ,"r") as infile:
    numOfWeights=int(infile.readline())
    numOfBiases=int(infile.readline())
    weights=[]
    biases=[]
    for _ in range(numOfWeights):
        numOfDim=int(infile.readline())
        shp=[0]*numOfDim
        for i in range(numOfDim):
            shp[i]=int(infile.readline())
        tempWt=np.zeros(np.prod(shp))
        for el in range(np.prod(shp)):
            tempWt[el]=float(infile.readline())
        weights.append(tempWt.reshape(shp))

    for _ in range(numOfBiases):
        numOfDim=int(infile.readline())
        shp=[0]*numOfDim
        for i in range(numOfDim):
            shp[i]=int(infile.readline())
        tempB=np.zeros(np.prod(shp))
        for el in range(np.prod(shp)):
            tempB[el]=float(infile.readline())
        biases.append(tempB.reshape(shp))


print(a)
print(b)

print("\n After reading \n")

print(weights)
print(biases)