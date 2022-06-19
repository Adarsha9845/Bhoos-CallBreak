from cards import Cards
from network import Network
import numpy as np

ip=60#number of input nodes
hidden1=100#first hidden layer
hidden2=50#first hidden layer
# hidden3=50#second hidden layer
op=52#number of output nodes in the layer


class Player:
    player_count = 0 #this is a static variable to count the number of players

    def __init__(self,initialization="gaussian",epsilon=0.01,alpha=0.001,gamma=1,value=None):
        '''
        value-> the value to be initialized into the weights
        '''
        self.epsilon=epsilon
        self.alpha=alpha
        self.gamma=gamma
        self.cards = 0 #all the cards that have been dealt to a player
        self.scores = [0]*5 # scores of all five round
        self.bid = 0 #bid made for the round
        self.roundScores = 0 #this contains the scores for the current round
        self.playerName = "P"+str(Player.player_count)
        # this is used to assign the player id and also count number of players
        Player.player_count += 1
        self.club = [] # All cards of suit club
        self.spade = [] # All cards of suit spade
        self.diamond = [] # All cards of suit diamond
        self.heart = [] # All cards of suit heart
        self.totalWins=0#this is the number of games won out of total rund
        self.previousQ = 0 # stores the previous Q values
        self.currentQ = 0 # stores the current Q values
        self.savedState=0
        self.R = 0 #most recent reward is saved
        self.network=Network([ip,hidden1,hidden2,op],initialization,value)
        self.gradients=0#stores the previous gradients for the update
        self.cardCounts=[0]*8#this consists of the values in following format::::
        self.historyOfQ=[]
        self.encodedVar = [1] * 52 # It is encoded input
        self.previousAction=0
        """
        [spades greater than our highest card, spades smaller than our highest card, spades, hearts
        greater than our highest heart card, hearts smaller than our highest heart card, club, diamond]
        ko format ma

        """

    def oneHotEncoder(actions):
        encodeVar = [0] * 52
        flag = 1
        for card in actions:
            suit = card[1]
            n = card[0]
            if suit == 'S':
                if n == '1' or n == '2' or n == '3' or n == '4' or n == '5' or n == '6' or n == '7' or n == '8' or n == '9':
                    encodeVar[int(n) - 1] = flag 

                elif n == 'T':
                    encodeVar[10 - 1] = flag

                elif n == 'J':
                    encodeVar[11 - 1] = flag

                elif n == 'Q':
                    encodeVar[12 - 1] = flag

                elif n == 'K':
                    encodeVar[13 - 1] = flag

            elif suit == 'H':
                if n == '1' or n == '2' or n == '3' or n == '4' or n == '5' or n == '6' or n == '7' or n == '8' or n == '9':
                    encodeVar[int(n) - 1 + 13] = flag 

                elif n == 'T':
                    encodeVar[10 - 1 + 13] = flag

                elif n == 'J':
                    encodeVar[11 - 1 + 13] = flag

                elif n == 'Q':
                    encodeVar[12 - 1 + 13] = flag

                elif n == 'K':
                    encodeVar[13 - 1 + 13] = flag

            elif suit == 'D':
                if n == '1' or n == '2' or n == '3' or n == '4' or n == '5' or n == '6' or n == '7' or n == '8' or n == '9':
                    encodeVar[int(n) - 1 + 13 * 2] = flag 

                elif n == 'T':
                    encodeVar[10 - 1 + 13 * 2] = flag

                elif n == 'J':
                    encodeVar[11 - 1 + 13 * 2] = flag

                elif n == 'Q':
                    encodeVar[12 - 1 + 13 * 2] = flag

                elif n == 'K':
                    encodeVar[13 - 1 + 13 * 2] = flag

            elif suit == 'D':
                if n == '1' or n == '2' or n == '3' or n == '4' or n == '5' or n == '6' or n == '7' or n == '8' or n == '9':
                    encodeVar[int(n) - 1 + 13 * 3] = flag 

                elif n == 'T':
                    encodeVar[10 - 1 + 13 * 3] = flag

                elif n == 'J':
                    encodeVar[11 - 1 + 13 * 3] = flag

                elif n == 'Q':
                    encodeVar[12 - 1 + 13 * 3] = flag

                elif n == 'K':
                    encodeVar[13 - 1 + 13 * 3] = flag

        return encodeVar

    def cardPlacing(self, suit, n, flag):
        # encoding in format [s, H, D, C]
        if suit == 'S':
            if n == '1' or n == '2' or n == '3' or n == '4' or n == '5' or n == '6' or n == '7' or n == '8' or n == '9':
                self.encodeVar[int(n) - 1] = flag 

            if n == 'T':
               self.encodeVar[10 - 1] = flag

            if n == 'J':
                self.encodeVar[11 - 1] = flag

            if n == 'Q':
                self.encodeVar[12 - 1] = flag

            if n == 'K':
                self.encodeVar[13 - 1] = flag

        if suit == 'H':
            if n == '1' or n == '2' or n == '3' or n == '4' or n == '5' or n == '6' or n == '7' or n == '8' or n == '9':
                self.encodeVar[int(n) - 1 + 13] = flag 

            if n == 'T':
                self.encodeVar[10 - 1 + 13] = flag

            if n == 'J':
                self.encodeVar[11 - 1 + 13] = flag

            if n == 'Q':
                self.encodeVar[12 - 1 + 13] = flag

            if n == 'K':
                self.encodeVar[13 - 1 + 13] = flag

        if suit == 'D':
            if n == '1' or n == '2' or n == '3' or n == '4' or n == '5' or n == '6' or n == '7' or n == '8' or n == '9':
                self.encodeVar[int(n) - 1 + 13 * 2] = flag 

            if n == 'T':
                self.encodeVar[10 - 1 + 13 * 2] = flag

            if n == 'J':
                self.encodeVar[11 - 1 + 13 * 2] = flag

            if n == 'Q':
                self.encodeVar[12 - 1 + 13 * 2] = flag

            if n == 'K':
                self.encodeVar[13 - 1 + 13 * 2] = flag

        if suit == 'D':
            if n == '1' or n == '2' or n == '3' or n == '4' or n == '5' or n == '6' or n == '7' or n == '8' or n == '9':
                self.encodeVar[int(n) - 1 + 13 * 3] = flag 

            if n == 'T':
                self.encodeVar[10 - 1 + 13 * 3] = flag

            if n == 'J':
                self.encodeVar[11 - 1 + 13 * 3] = flag

            if n == 'Q':
                self.encodeVar[12 - 1 + 13 * 3] = flag

            if n == 'K':
                self.encodeVar[13 - 1 + 13 * 3] = flag

        return self.encodeVar
      

#only call the function once once the card in distributed and we have 13 cards in our hand..
    def ourCardIni(self):

        for card in self.cards:
            self.encodedVar = self.cardPlacing(card[1], card[0], 2)
            
    def resetPlayer(self,count):
        if ((count+1)%100)==0:
            # print(f"The value of count is::::{count}")
            self.saveWeightsNBiases()
        self.cards = 0
        self.scores = [0]*5
        self.bid = 0
        self.roundScores = 0
        self.club = []
        self.spade = []
        self.diamond = []
        self.heart = []
        self.previousQ = 0
        self.currentQ = 0
        self.R = 0 #most recent reward is saved
        self.gradients=0#stores the previous gradients for the update
        self.cardCounts=[0]*8
        self.encodedVar=[1]*52


    def saveWeightsNBiases(self):
        fileName=self.playerName+".nt"
        a=self.network.weights
        b=self.network.biases

        with open(fileName,"w") as outfile:
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

    def readWeightsNBiases(self,player="default"):
        if player=='default':
            fileName=self.playerName+".nt"
        else:
            fileName=player+".nt"
        with open(fileName ,"r") as infile:
            # reading the number of weights and biases
            numOfWeights=int(infile.readline())
            numOfBiases=int(infile.readline())
            #reading the weights first
            for j in range(numOfWeights):
                # reading the nubmer of dimensions
                numOfDim=int(infile.readline())
                shp=[0]*numOfDim
                # reading the value of each dimension
                for i in range(numOfDim):
                    shp[i]=int(infile.readline())
                # initializing the temporary array of required size with zeros
                tempWt=np.zeros(np.prod(shp))
                # putting into the space the values of various index
                for el in range(np.prod(shp)):
                    tempWt[el]=float(infile.readline())
                # making a hard copy of the obtained weights into the weight list
                self.network.weights[j]=tempWt.reshape(shp).copy()

            for j in range(numOfBiases):
                #the steps are same as above, that of weights
                numOfDim=int(infile.readline())
                shp=[0]*numOfDim
                for i in range(numOfDim):
                    shp[i]=int(infile.readline())
                tempB=np.zeros(np.prod(shp))
                for el in range(np.prod(shp)):
                    tempB[el]=float(infile.readline())
                self.network.biases[j]=tempB.reshape(shp)
                
    def giveBid(self, risk_factor):
        # risk_factor determines the optimism of the bid
        spadeGone = 0
        numS=len(self.spade)
        bid_H, spadeGone = self.bidH(self.heart, len(self.heart), numS, risk_factor)
        numS = numS - spadeGone
        bid_D, spadeGone = self.bidD(self.diamond,len(self.diamond), numS, risk_factor)
        numS = numS - spadeGone
        bid_C, spadeGone = self.bidC(self.club,len(self.club), numS, risk_factor)
        numS = numS - spadeGone
        bid_S = self.bidS(self.spade,len(self.spade), risk_factor)
        self.bid=bid_H+bid_D+bid_C+bid_S
        if self.bid<1:
            self.bid=1
        elif self.bid>8:
            self.bid=8
        return self.bid  # this has to be setup later using RL

    def playCard(self, playContext,train,lossFn,delta):
        self.previousQ = self.currentQ
        actions = self.possibleCards(playContext["played"])# this is the list of possible actions from the 
                                                           # cards available with us
        
        inputs=[self.input_encoding(playContext)]#this is the input of dimension 1*60

        z,a=self.network.feedForward(np.array(inputs))
        #the q values are the output of the neural network of the size 1x52
        qvalues=a[-1].tolist()

        #we need to modify below this###########
        actionsEncoding=self.oneHotEncoder(actions)

        actionsEncodingBool=[bool(x) for x in actionsEncoding]
        
        possibleActionsQValues=np.array(qvalues)[actionsEncodingBool].tolist()

        option = np.random.random()
        if option <= self.epsilon:  # exploration
            index = np.random.randint(len(possibleActionsQValues))
            action=qvalues.index(possibleActionsQValues[index])
        else:  # exploitation
            action = qvalues.index(max(possibleActionsQValues))

        hand = actions[action]# need to select this with reverse encoding

        self.historyOfQ.append(qvalues[action])#for plotting purposes

        target=[0]*52
        target[self.previousAction]=max(qvalues)*self.gamma+self.R
        if len(self.cards) < 13 and train:
            b,w=self.gradients#this can be done only after the first iteration
            for _ in 10:# here epochs=10
                a,z=self.network.feedForward(np.array(self.savedState))
                # need to update this for each of the weights
                if lossFn=='huber':
                    tempVal=np.array(target).reshape(1,-1)-a[-1]
                    tempVal=np.where(tempVal<=delta,tempVal,delta)
                    for i in range(len(w)):
                        self.network.biases[i]=self.network.biases[i]+self.alpha * \
                            np.sum(b[i]*tempVal,axis=0)
                        self.network.weights[i] =self.network.weights[i] +self.alpha * \
                            tempVal*w[i]
                else:
                    tempVal=self.R+self.gamma*max(qvalues)-self.previousQ
                    for i in range(len(w)):
                        self.network.biases[i]=self.network.biases[i]+self.alpha * \
                            (tempVal-self.previousQ)*b[i]
                        self.network.weights[i] =self.network.weights[i] +self.alpha * \
                            (tempVal-self.previousQ)*w[i]
        #######
        self.gradients=self.network.gradient(a, z)#these gradients will be used in the next loop
                                                  #these are the gradients of biases and weights
        self.previousAction=action
        self.savedState=inputs
        
        
        card2play = hand
        self.suitCards(card2play[1]).remove(card2play)
        # need to make ammends to update the individual lists as well
        return self.cards.pop(self.cards.index(card2play))

    def dealtCards(self, cards):
        """This is called at the beginning when we have to distribute the cards to players"""
        self.cards = cards
        self.heart=[]
        self.club=[]
        self.spade=[]
        self.diamond=[]
        for card in cards:
            if card[1] == "H":
                self.heart.append(card)
            elif card[1] == "S":
                self.spade.append(card)
            elif card[1] == "D":
                self.diamond.append(card)
            else:
                self.club.append(card)

        self.ourCardIni()


    def suitCards(self, suit):
        if suit == "H":
            return self.heart
        if suit == "C":
            return self.club
        if suit == "D":
            return self.diamond
        else:
            return self.spade

    def highestSuitCard(self, suit):
        cards=self.suitCards(suit)
        if len(cards)==0:
            return None
        highest=cards[0]
        for card in cards[1:]:
            if Cards.getRank(card)["value"]>Cards.getRank(highest)["value"]:
                highest=card
        return highest

    def terminalUpdate(self):
        self.previousQ = self.currentQ
        b,w=self.gradients
        for i in range(len(w)):
                self.network.biases[i]=self.network.biases[i]+self.alpha*(self.R-self.previousQ)*b[i]
                self.network.weights[i]=self.network.weights[i] +self.alpha*(self.R-self.previousQ)*w[i]

    def bidC(self,card_C, num_c, num_S, risk_factor):
        aa = 0
        bid_C = 0
        spade_gone = 0
        for card in card_C:
            if num_c == 1:
                if card[0] == '1':
                    bid_C = bid_C + 1
                    if num_S == 1:
                        bid_C = bid_C + 1
                        spade_gone = spade_gone + 1

                    if num_S >= 2:
                        bid_C = bid_C + 2
                        spade_gone = spade_gone + 2
            if num_c == 0:
                if num_S == 1:
                    bid_C = bid_C + 1
                    spade_gone = spade_gone + 1
                if num_S == 2:
                    bid_C = bid_C + 2
                    spade_gone = spade_gone + 2
                if num_S >= 3:
                    bid_C = bid_C + 3
                    spade_gone = spade_gone + 3

            if num_c == 2 and card[0] != 'K' and card[0] != 'A' and aa == 0:
                if num_S >= 1:
                    bid_C = bid_C + 1 * risk_factor
                    spade_gone = spade_gone + 1 * risk_factor
                    aa = 1

            if num_c == 3:
                if card[0] == 'Q':
                    bid_C = bid_C + 1 * risk_factor

            if num_c >= 2 and num_c <= 5:
                if card[0] == '1':
                    bid_C = bid_C + 1
                if card[0] == 'K':
                    bid_C = bid_C + 1

            if num_c >= 6 and num_c <= 8:
                if card[0] == '1':
                    bid_C = bid_C + 1

        return [bid_C, spade_gone]

    def bidD(self,card_D, num_D, num_S, risk_factor):
        bid_D = 0
        spade_gone = 0
        aa = 0
        for card in card_D:
            if num_D == 1:
                if card[0] == '1':
                    bid_D = bid_D + 1
                if num_S == 1:
                    bid_D = bid_D + 1
                    spade_gone = spade_gone + 1
                if num_S >= 2:
                    bid_D = bid_D + 2
                    spade_gone = spade_gone + 2
                if num_D == 0:
                    if num_S == 1:
                        bid_D = bid_D + 1
                        spade_gone = spade_gone + 1
                    if num_S == 2:
                        bid_D = bid_D + 2
                        spade_gone = spade_gone + 2
                    if num_S >= 3:
                        bid_C = bid_C + 3
                        spade_gone = spade_gone + 3

            if num_D == 2 and card[0] != 'K' and card[0] != 'A' and aa == 0:
                if num_S >= 1:
                    bid_D = bid_D + 1 * risk_factor
                    spade_gone = spade_gone + 1 * risk_factor
                    aa = 1

            if num_D == 3:
                if card[0] == 'Q':
                    bid_D = bid_D + 1 * risk_factor

            if num_D >= 2 and num_D <= 5:
                if card[0] == '1':
                    bid_D = bid_D + 1
                if card[0] == 'K':
                    bid_D = bid_D + 1

            if num_D >= 6 and num_D <= 8:
                if card[0] == '1':
                    bid_D = bid_D + 1
        return [bid_D, spade_gone]

    def bidH(self,card_H, num_H, num_S, risk_factor):
        bid_H = 0
        spade_gone = 0
        aa = 0
        for card in card_H:
            if num_H == 1:
                if card[0] == '1':
                    bid_H = bid_H + 1
                if num_S == 1:
                    bid_H = bid_H + 1
                    spade_gone = spade_gone + 1
                if num_S >= 2:
                    bid_H = bid_H + 2
                    spade_gone = spade_gone + 2
            if num_H == 0:
                if num_S == 1:
                        bid_H = bid_H + 1
                        spade_gone = spade_gone + 1
                if num_S == 2:
                    bid_H = bid_H + 2
                    spade_gone = spade_gone + 2
                if num_S >= 3:
                    bid_C = bid_C + 3
                    spade_gone = spade_gone + 3

            if num_H == 2 and card[0] != 'K' and card[0] != 'A' and aa == 0:
                if num_S >= 1:
                    bid_H = bid_H + 1 * risk_factor
                    spade_gone = spade_gone + 1 * risk_factor
                    aa = 1

            if num_H == 3:
                if card[0] == 'Q':
                    bid_H = bid_H + 1 * risk_factor

            if num_H >= 2 and num_H <= 5:
                if card[0] == '1':
                    bid_H = bid_H + 1
                if card[0] == 'K':
                    bid_H = bid_H + 1

            if num_H >= 6 and num_H <= 8:
                if card[0] == '1':
                    bid_H = bid_H + 1
        return [bid_H, spade_gone]
    
    def bidS(self,card_S, num_S, risk_factor):
        bid_S = 0
        spade_gone = 0
        if num_S >= 1:
            for card in card_S:
                if card[0] == '1':
                    bid_S = bid_S + 1

                if num_S >= 2:
                    if card[0] == 'K':
                        bid_S = bid_S + 1
                    

                if num_S >=3:
                    if card[0] == 'Q':
                        bid_S = bid_S + 1

            if num_S >= 4:
                bid_S = bid_S + num_S - 3


        return bid_S
    
    def handWinReward(self):#used
        # print("the hand reward for "+ self.playerName)
        self.R=1

    def bidReward(self,condition):#used
        # print("the bid reward for "+ self.playerName)
        if condition=="equal":
            self.R+=2*self.bid
        elif condition=="greater":
            self.R+=self.bid
        else:
            self.R+=-2*self.bid

    def possibleCards(self,played):
        if len(played)==0:
            return self.cards
        firstCard=played[0]      
        playable=[]

        if len(played)==1:
            temp=self.suitCards(firstCard[1])
            if len(temp)!=0:
                for card in temp:
                    if Cards.getRank(card)["value"]>Cards.getRank(firstCard)["value"]:
                        playable.append(card)
                if len(playable)==0:
                    playable=temp
            else:
                playable=self.suitCards('S')
                if len(playable)==0:
                    playable=self.cards        
        elif len(played)==2:
            secondCard=played[1]
            temp=self.suitCards(firstCard[1])
            if len(temp)!=0:
                if secondCard[1]==firstCard[1]:
                    for card in temp:
                        if Cards.getRank(card)["value"]>Cards.getRank(firstCard)["value"] and\
                            Cards.getRank(card)["value"]>Cards.getRank(secondCard)["value"]:
                            playable.append(card)
                    if len(playable)==0:
                        playable=temp
                elif secondCard[1]=="S":
                    playable=temp
                else:
                    playable=[card for card in temp if Cards.getRank(card)["value"]>Cards.getRank(firstCard)["value"]]
                    if len(playable)==0:
                        playable=temp    
            else:
                temp=self.suitCards('S')
                if secondCard[1]=="S":
                    for card in temp:
                        if Cards.getRank(card)["value"]>Cards.getRank(secondCard)["value"]:
                            playable.append(card)
                    if len(playable)==0:
                        playable=self.cards
                else:
                    playable=temp
                if len(playable)==0:
                    playable=self.cards
        else:
            secondCard=played[1]
            thirdCard=played[2]
            temp=self.suitCards(firstCard[1])
            if len(temp)!=0:
                if secondCard[1]==firstCard[1] and thirdCard[1]==firstCard[1]:
                    for card in temp:
                        if Cards.getRank(card)['value']>Cards.getRank(firstCard)['value'] and\
                            Cards.getRank(card)['value']>Cards.getRank(secondCard)['value'] and \
                                Cards.getRank(card)['value']>Cards.getRank(thirdCard)['value']:
                            playable.append(card)
                    if len(playable)==0:
                        playable=temp
                elif secondCard[1]!=firstCard[1] and thirdCard[1]==firstCard[1]:
                    for card in temp:
                        if Cards.getRank(card)['value']>Cards.getRank(firstCard)['value'] and\
                            Cards.getRank(card)['value']>Cards.getRank(thirdCard)['value']:
                            playable.append(card)
                    if len(playable)==0:
                        playable=temp
                elif secondCard[1]==firstCard[1] and thirdCard[1]!=firstCard[1]:
                    for card in temp:
                        if Cards.getRank(card)['value']>Cards.getRank(firstCard)['value'] and\
                            Cards.getRank(card)['value']>Cards.getRank(secondCard)['value']:
                            playable.append(card)
                    if len(playable)==0:
                        playable=temp
                elif secondCard[1]=="S" or thirdCard[1]=="S":
                    playable=temp
                else:
                    for card in temp:
                        if Cards.getRank(card)['value']>Cards.getRank(firstCard)['value']:
                            playable.append(card)                    
                    if len(playable)==0:
                        playable=temp


            else:
                temp=self.suitCards('S')
                if len(temp)!=0:
                    if secondCard[1]=="S" and thirdCard[1]=="S":
                        for card in temp:
                            if Cards.getRank(card)["value"]>Cards.getRank(secondCard)["value"] and\
                                Cards.getRank(card)["value"]>Cards.getRank(thirdCard)["value"]:
                                playable.append(card)
                    elif secondCard[1]=="S" and thirdCard[1]!="S":
                        for card in temp:
                            if Cards.getRank(card)["value"]>Cards.getRank(secondCard)["value"]:                        playable.append(card)
                    elif secondCard[1]!="S" and thirdCard[1]=="S":
                        for card in temp:
                            if Cards.getRank(card)["value"]>Cards.getRank(thirdCard)["value"]:
                                playable.append(card)
                    else:
                        playable=temp
                    if len(playable)==0:
                        playable=self.cards
                else:
                    if len(temp)==0:
                        playable=self.cards
        return playable

    def cardEncoding(self, history, played):
        for card in played:
            self.encodedVar = self.cardPlacing(card[1], card[0], -1)

        for card in history[1]:
            self.encodedVar = self.cardPlacing(card[1], card[0], -2)

        return self.encodedVar


    def playedCard(self,played):
        played_card = [0] * 6
        counter = 0
        for card in played:
            played_card[counter] = Cards.getRank(card)['value']
            counter = counter + 1
            played_card[counter] = Cards.getSuit(card)['value']
            counter = counter + 1
        return played_card

    def largestSmallestNumFunc(self,history):
        suits=['S','H','C','D']
        if len(history)==0:
            for i in range(4):
                self.cardCounts[i*2]=14-Cards.getRank(self.highestSuitCard(suits[i]))["value"]
                self.cardCounts[i*2+1]=np.abs(Cards.getRank(self.highestSuitCard(suits[i]))["value"]-2)
        else:
            for card in history[-1][1]:
                suitValue=Cards.getSuit(card)["value"]#this is the value of the suit, spade ko 1
                highestCardValue=Cards.getRank(self.highestSuitCard(suits[suitValue-1]))["value"]
                #this is the value of the highest card of the suit that is being thrown
                if Cards.getRank(card)["value"]>highestCardValue:
                    #if the card thrown has higher value, it decreases the count of card
                    #greater than our highest card by one which is done over here
                    self.cardCounts[suitValue*2-2]-=1
                else:
                    self.cardCounts[suitValue*2-1]-=1
        return self.cardCounts


    def possibleMoveEnc(self,possibleMove):
        encod_possible = [0] * 2
        encod_possible[0] = Cards.getRank(possibleMove)['value']
        encod_possible[1] = Cards.getSuit(possibleMove)['value']
        return encod_possible

    # Possible_move is a possible card suggested..
    def input_encoding(self, playInfo):
        # remaining card in the hand..
        # print('...................')
        # print(playInfo['history'])
        if len(playInfo['history']) == 0:
            largestSmallestNum = self.largestSmallestNumFunc(playInfo['history'])

        if len(playInfo['history']) != 0:

            self.encodedVar = self.cardEncoding(playInfo['history'][-1], playInfo['played'])
            # played card in the order..
            # played_card = self.playedCard(playInfo['played'])
            #Largest and Smallest number of card than ours largest card..
            largestSmallestNum = self.largestSmallestNumFunc(playInfo['history'])
            # possibleMove = self.possibleMoveEnc(possible_move)

        # finalInputEncoding = my_card+played_card+largestSmallestNum+possibleMove
        finalInputEncoding = largestSmallestNum + self.encodedVar
    
        return finalInputEncoding



