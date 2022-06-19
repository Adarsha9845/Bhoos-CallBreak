import numpy as np
from requests import check_compatibility
from cards import Cards
import matplotlib.pyplot as plt


numOfCards=13

class GameMaster:
    round = 0
    bids=[0,0,0,0]#stores bids according to the order static variable
    sequence = [0, 1, 2, 3]  # this is the sequence of players who throw card
    history = []
    order=[]
    lastRoundWinner = None #this is used as the previous winner in a set of 4 cards regardless of rounds
    playInfo = {
        "timeBudget": None,  # float
        "playerId": None,  # string
        # 4 strings
        "playerIds": [
            "P0",
            "P1",
            "P2",
            "P3"
        ],
        #  upto 13 cards in string format
        "cards": [],
        #  upto 3 cards in order from last winner
        #  last winner can be inferred from last item in history
        #  e.g > payload.history[payload.history.length - 1][2]
        "played": [],
        #  'history' field contains an ordered list of cards played from first hand.
        #  Format: 'start idx, [cards in clockwise order of player ids], winner idx'
        #  'start idx' is index of player that threw card first
        #  'winner idx' is index of player who won this hand
        "history": [],
        #  Context has metadata about the current round:
        #  'ruond': the current round[1 - 5]
        #  'totalPoints': the points accumulated till this round(dhoos is also subtracted)
        #  'bid': bid of current round
        #  'won': total hands won this round upto this point
        "context": {
            "round": 0,
            "players": {
                "P0": {
                    "totalPoints": 0,
                    "bid": 0,
                    "won": 0
                },
                "P1": {
                    "totalPoints": 0,
                    "bid": 0,
                    "won": 0
                },
                "P2": {
                    "totalPoints": 0,
                    "bid": 0,
                    "won": 0
                },
                "P3": {
                    "totalPoints": 0,
                    "bid":0,
                    "won":0
                }
            }
        }
    }
    bidInfo = {
        #    timeBudget left for this round, time alloted for bid + play 12 hands
        "timeBudget": None,
        #    current player's string; this is your id
        "playerId": None,
        #    4 strings
        "playerIds": ["P0", "P1", "P2", "P3"],
        #    13 cards in string format
        "cards": [],
        #    Context has metadata about the current round:
        #  'ruond': the current round [1 - 5]
        #  'totalPoints': the points accumulated till this round (dhoos is also subtracted)
        #  'bid': bid of current round
        #  'won': total hands won this round upto this point
        "context": {
            "round": 0,
            "players": {
                "P0": {
                    "totalPoints": 0,
                    "bid": 0,
                    "won": 0
                },
                "P1": {
                    "totalPoints": 0,
                    "bid": 0,
                    "won": 0
                },
                "P2": {
                    "totalPoints": 0,
                    "bid": 0,
                    "won": 0
                },
                "P3": {
                    "totalPoints": 0,
                    "bid": 0,
                    "won": 0
                }
            }
        }
    }

    @staticmethod
    def resetGameMaster():
        GameMaster.round = 0
        GameMaster.bids=[0,0,0,0]#stores bids according to the order static variable
        GameMaster.sequence = [0, 1, 2, 3]  # this is the sequence of players who throw card
        GameMaster.history = []
        GameMaster.order=[]
        GameMaster.lastRoundWinner = None #this is used as the previous winner in a set of 4 cards regardless of rounds
        GameMaster.playInfo = {
            "timeBudget": None,  # float
            "playerId": None,  # string
            # 4 strings
            "playerIds": [
                "P0",
                "P1",
                "P2",
                "P3"
            ],
            #  upto 13 cards in string format
            "cards": [],
            #  upto 3 cards in order from last winner
            #  last winner can be inferred from last item in history
            #  e.g > payload.history[payload.history.length - 1][2]
            "played": [],
            #  'history' field contains an ordered list of cards played from first hand.
            #  Format: 'start idx, [cards in clockwise order of player ids], winner idx'
            #  'start idx' is index of player that threw card first
            #  'winner idx' is index of player who won this hand
            "history": [],
            #  Context has metadata about the current round:
            #  'ruond': the current round[1 - 5]
            #  'totalPoints': the points accumulated till this round(dhoos is also subtracted)
            #  'bid': bid of current round
            #  'won': total hands won this round upto this point
            "context": {
                "round": 0,
                "players": {
                    "P0": {
                        "totalPoints": 0,
                        "bid": 0,
                        "won": 0
                    },
                    "P1": {
                        "totalPoints": 0,
                        "bid": 0,
                        "won": 0
                    },
                    "P2": {
                        "totalPoints": 0,
                        "bid": 0,
                        "won": 0
                    },
                    "P3": {
                        "totalPoints": 0,
                        "bid":0,
                        "won":0
                    }
                }
            }
        }
        GameMaster.bidInfo = {
        #    timeBudget left for this round, time alloted for bid + play 12 hands
        "timeBudget": None,
        #    current player's string; this is your id
        "playerId": None,
        #    4 strings
        "playerIds": ["P0", "P1", "P2", "P3"],
        #    13 cards in string format
        "cards": [],
        #    Context has metadata about the current round:
        #  'ruond': the current round [1 - 5]
        #  'totalPoints': the points accumulated till this round (dhoos is also subtracted)
        #  'bid': bid of current round
        #  'won': total hands won this round upto this point
        "context": {
            "round": 0,
            "players": {
                "P0": {
                    "totalPoints": 0,
                    "bid": 0,
                    "won": 0
                },
                "P1": {
                    "totalPoints": 0,
                    "bid": 0,
                    "won": 0
                },
                "P2": {
                    "totalPoints": 0,
                    "bid": 0,
                    "won": 0
                },
                "P3": {
                    "totalPoints": 0,
                    "bid": 0,
                    "won": 0
                }
            }
        }
    }

    @staticmethod
    def distribute():
        while(True):
            idx = np.random.permutation(52)
            allCards = Cards.createCombo()
            np.random.shuffle(allCards)
            p1 = [allCards[i] for i in idx[0:13]]
            p2 = [allCards[i] for i in idx[13:26]]
            p3 = [allCards[i] for i in idx[26:39]]
            p4 = [allCards[i] for i in idx[39:52]]
            if GameMaster.checkCards([p1,p2,p3,p4]):
                break                      
        return p1, p2, p3, p4

    @staticmethod
    def checkCards(deck):
        for group in deck:
            spade=0
            face=0
            for card in group:
                if card[1]=="S":
                    spade+=1
                if card[0]=="J" or card[0]=="Q" or card[0]=="K":
                    face+=1
                if spade>0 and face>0:
                    return True
            if spade==0 or face==0:
                return False

    @staticmethod
    def setupOrder():
        if GameMaster.lastRoundWinner==None:
            GameMaster.order=[(GameMaster.round-1+a)%4 for a in range(4)]
        else:
            GameMaster.order=[(GameMaster.order[GameMaster.lastRoundWinner]+a)%4 for a in range(4)]

    @staticmethod
    def biddingPhase(players,printBidInfo=False,riskFactor=1):#order represents the order in which the bids are to be made
        # and cards are to be thrown
        GameMaster.setupOrder()
        for playerNum in GameMaster.order:
            GameMaster.updateBidInfo(players[playerNum])
            while True:
                # print("Asking bid from player"+players[playerNum].playerName)
                bid=players[playerNum].giveBid(riskFactor)
                if bid>=1 and bid<=8:
                    break
                else:
                    print(f"\n{players[playerNum].playerName} input invalid bid!!!!")
            GameMaster.bidInfo["context"]["players"][players[playerNum].playerName]["bid"]=bid
            GameMaster.playInfo["context"]["players"][players[playerNum].playerName]["bid"]=bid
            GameMaster.bids[playerNum]=bid#this stores bid acc to the values in the variable order
        if printBidInfo:
            print("Bids made by various players are as follows:\n")
            print(GameMaster.bidInfo)
            print("----------")

    @staticmethod
    def updateBidInfo(player):
        GameMaster.bidInfo["playerId"]=player.playerName
        GameMaster.bidInfo["cards"]=player.cards
        GameMaster.bidInfo["context"]["round"]=GameMaster.round
    
    @staticmethod
    def oneRound(players,printHistory=False,train=True,lossFn='huber',delta=0.02):
        """
        printHistory: this prints the history which can be used to check if the cards thrown
                        is correct; this is used after training of weights 
        train: this value denotes whether the weights are to be upgraded
        lossFn: two loss functions are available: mean squared error and huber
        delta: this is the parameter of huber loss and by default equal to 0.02
        """
        for i in range(numOfCards):
            # print("Hand%d"%(i+1))
            if i!=0:
                GameMaster.setupOrder()
            for playerNum in GameMaster.order:
                GameMaster.updatePlayInfo(players[playerNum])

                cardResponse=players[playerNum].playCard(GameMaster.playInfo,train,lossFn,delta)
                #need to remove the used card here and add validation as well
                if not GameMaster.checkCompatibility(cardResponse):
                    print(GameMaster.playInfo)
                    print(cardResponse)
                    raise("!!!Invalid Move!!!!")
                GameMaster.playInfo["played"].append(cardResponse)
            
            GameMaster.lastRoundWinner=GameMaster.winCondition()
            
            #the last round winner will be the position of the card in the Gamemaster.playInfo["played"]
            #and the order list will also have to be used to determine the winner
            GameMaster.history.append([GameMaster.order[0],GameMaster.playInfo["played"],\
                                            GameMaster.order[GameMaster.lastRoundWinner]])
            GameMaster.playInfo["history"]=GameMaster.history
            if printHistory:#if asked by the user then prints the history
                print("Moves played:")
                print(GameMaster.playInfo["history"][-1])
                print("----------")
            GameMaster.playInfo["played"]=[]
                        
            winPlayer=players[GameMaster.order[GameMaster.lastRoundWinner]]#winner player
            winPlayer.roundScores+=1
            GameMaster.playInfo["context"]["players"][winPlayer.playerName]["won"]+=1
            GameMaster.bidInfo["context"]["players"][winPlayer.playerName]["won"]+=1

            #reward function is added here(only hand win reward and bidreward are used here)
            players[GameMaster.order[GameMaster.lastRoundWinner]].handWinReward()
            if i==12:
                # print("Here is the history of the round")
                # print(GameMaster.playInfo["history"])
                # print("end of play context")
                GameMaster.scoreUpdate(players)
                GameMaster.cleaningPerRound(players)#context and variables are updated
                # print("Here is the playCOntext of the round")
                # print(GameMaster.playInfo)
                # print("end of play context")
                
                #this part assigns reward after each of the rounds
                roundRewards=[]
                for player in players:
                    roundRewards.append(player.scores[GameMaster.round-1])
                GameMaster.roundWinReward(players[roundRewards.index(max(roundRewards))])
                #####
                if GameMaster.round==5:
                    # we calculate the total scores at the end of 5th round
                    finalScores=[]
                    for player in players:
                        finalScores.append(sum(player.scores))
                    gameWinner=finalScores.index(max(finalScores))
                    GameMaster.gameWinReward(players[gameWinner])
                    players[gameWinner].totalWins+=1
                    #overall winner information
                    print(f"The overall winner is {players[gameWinner].playerName} with score {finalScores}")
                if train:
                    for player in players:
                        player.terminalUpdate()    
                        
            ######end of reward function######

    @staticmethod
    def updatePlayInfo(player):
        GameMaster.playInfo["playerId"]=player.playerName
        GameMaster.playInfo["cards"]=player.cards
        GameMaster.playInfo["context"]["round"]=GameMaster.round
    

    @staticmethod
    def winCondition():
        # """THis could have been def winCondition(played) to check the working"""
        played=GameMaster.playInfo["played"]
        spades=[]
        firstSuit=[]
        for card in played:
            if card[1]=="S":
                spades.append(card)
            elif card[1]==played[0][1]:
                firstSuit.append(card)
        winner=0
        if len(spades)!=0:
            winner=spades[0]
            for card in spades[1:]:
                if Cards.getRank(card)["value"]>Cards.getRank(winner)["value"]:
                    winner=card
        elif len(firstSuit)>=1:
            winner = firstSuit[0]
            for card in firstSuit[1:]:
                if Cards.getRank(card)["value"]>Cards.getRank(winner)["value"]:
                    winner=card
        return played.index(winner)
        # return 1

    @staticmethod
    def scoreUpdate(players):
        for player in players:
            if player.roundScores==player.bid:
                player.scores[GameMaster.round-1]=player.roundScores
                player.bidReward("equal")
            elif player.roundScores>player.bid:
                player.scores[GameMaster.round-1]=player.bid+(player.roundScores-player.bid)/10
                player.bidReward("greater")
            else:
                player.scores[GameMaster.round-1]=-player.bid
                player.bidReward("less")
            GameMaster.bidInfo["context"]["players"][player.playerName]["totalPoints"]+=player.scores[GameMaster.round-1]
            GameMaster.playInfo["context"]["players"][player.playerName]["totalPoints"]+=player.scores[GameMaster.round-1]



    @staticmethod
    def cleaningPerRound(players):
        #for cleaning after each round->bids and wons per round are cleaned, history is also cleared
        for player in players:
            player.roundScores=0
            player.bid=0
            GameMaster.bidInfo["context"]["players"][player.playerName]["bid"]=0
            GameMaster.bidInfo["context"]["players"][player.playerName]["won"]=0
            GameMaster.playInfo["context"]["players"][player.playerName]["bid"]=0
            GameMaster.playInfo["context"]["players"][player.playerName]["won"]=0
            GameMaster.playInfo["history"]=[]
            GameMaster.history=[]
            GameMaster.lastRoundWinner=None

    @staticmethod
    def checkCompatibility(response):#plyayed hatauna parcha ya
        played=GameMaster.playInfo["played"]
        # if not response in GameMaster.playInfo["cards"]:
        #     return False
        # else:
        #     GameMaster.playInfo["cards"].remove(response)
        if len(played)==0:
            return True
        elif len(played)==1:#this checks the condition for only one player prior to us

            remaining=GameMaster.playInfo["cards"]#these are the remaining cards with the player after throwing the response
            firstCard=played[0]#first card played by the first player
            if Cards.getSuit(response)["code"]==Cards.getSuit(firstCard)["code"]:
                if Cards.getRank(response)["value"]>Cards.getRank(firstCard)["value"]:
                    return True
                else:
                    for card in remaining:
                        if Cards.getSuit(card)["code"]==Cards.getSuit(firstCard)["code"]:
                            if Cards.getRank(card)["value"]>Cards.getRank(firstCard)["value"]:
                                return False
                    return True
            else:
                for card in remaining:
                    if Cards.getSuit(card)["code"]==Cards.getSuit(firstCard)["code"]:
                        return False 
                if Cards.getSuit(response)["code"]!="S":
                    for card in remaining:
                        if Cards.getSuit(card)["code"]=="S":
                            return False
                return True
        elif len(played)==2:#this checks the condition for two players who have played before us
            remaining=GameMaster.playInfo["cards"]#these are the remaining cards with the player after throwing the response
            firstCard=played[0]#first card played by the first player
            secondCard=played[1]#second card played

            if firstCard[1]==secondCard[1]:
                if response[1]==firstCard[1]:
                    if Cards.getRank(response)["value"]>Cards.getRank(firstCard)["value"] and \
                       Cards.getRank(response)["value"]>Cards.getRank(secondCard)["value"]: 
                        return True
                    else:
                        for card in remaining:
                            if card[1]==response[1]:
                                if Cards.getRank(card)["value"]>Cards.getRank(firstCard)["value"] and \
                                    Cards.getRank(card)["value"]>Cards.getRank(secondCard)["value"]: 
                                    return False
                        return True
                else:
                    if response[1]=="S":
                        for card in remaining:
                            if card[1]==secondCard[1]:
                                return False
                        return True
                    else:
                        for card in remaining:
                            if card[1]==secondCard[1] or card[1]=="S":
                                return False
                        return True
            else:
                if secondCard[1]=="S":
                    if response[1]==firstCard[1]:
                        return True
                    elif response[1]=="S":
                        for card in remaining:
                            if card[1]==firstCard[1]:
                                return False
                        if Cards.getRank(response)["value"]>Cards.getRank(secondCard)["value"]:
                            return True
                        else:
                            for card in remaining:
                                if card[1]=="S":
                                    if Cards.getRank(card)["value"]>Cards.getRank(secondCard)["value"]:
                                        return False
                            return True
                    else:
                        for card in remaining:
                            if card[1]==firstCard[1]:
                                return False
                            elif card[1]=="S":
                                if Cards.getRank(card)["value"]>Cards.getRank(secondCard)["value"]:
                                    return False
                        return True
                else:
                    if response[1]==firstCard[1]:
                        if Cards.getRank(response)["value"]>Cards.getRank(firstCard)["value"]:
                            return True
                        else:
                            for card in remaining:
                                if card[1]==firstCard[1]:
                                    if Cards.getRank(card)["value"]>Cards.getRank(firstCard)["value"]:
                                        return False
                            return True
                    elif response[1]=="S":
                        for card in remaining:
                            if card[1]==firstCard[1]:
                                return False
                        return True
                    else:
                        for card in remaining:
                            if card[1]=="S" or card[1]==firstCard[1]:
                                return False
                        return True
        elif len(played)==3:
            remaining=GameMaster.playInfo["cards"]#these are the remaining cards with the player after throwing the response
            firstCard=played[0]#first card played by the first player
            secondCard=played[1]#second card played
            thirdCard=played[2]#third card played
            if firstCard[1]==secondCard[1]:
                if secondCard[1]==thirdCard[1]:
                    if response[1]==firstCard[1]:
                        if Cards.getRank(response)["value"]>Cards.getRank(thirdCard)["value"] and\
                            Cards.getRank(response)["value"]>Cards.getRank(secondCard)["value"] and\
                                Cards.getRank(response)["value"]>Cards.getRank(firstCard)["value"]:
                            
                            return True
                        else:
                            for card in remaining:
                                if card[1]==firstCard[1]:
                                    if Cards.getRank(card)["value"]>Cards.getRank(thirdCard)["value"] and\
                                        Cards.getRank(card)["value"]>Cards.getRank(secondCard)["value"] and\
                                        Cards.getRank(card)["value"]>Cards.getRank(firstCard)["value"]:
                                        return False
                            return True
                    elif response[1]=="S":
                        for card in remaining:
                            if card[1]==firstCard[1]:
                                return False
                        return True
                    else:
                        for card in remaining:
                            if card[1]=="S" or card[1]==firstCard[1]:
                                return False
                        return True
                elif thirdCard[1]=="S":
                    if response[1]==firstCard[1]:
                        return True
                    elif response[1]=="S":
                        for card in remaining:
                            if card[1]==firstCard[1]:
                                return False
                        if Cards.getRank(response)["value"]>Cards.getRank(thirdCard)["value"]:
                            return True
                        else:
                            for card in remaining:
                                if card[1]=="S":
                                    if Cards.getRank(card)["value"]>Cards.getRank(thirdCard)["value"]:
                                        return False
                            return True
                    else:
                        for card in remaining:
                            if card[1]==firstCard[1]:
                                return False
                            if card[1]=='S' and Cards.getRank(card)["value"]>Cards.getRank(thirdCard)["value"]:
                                return False 
                        return True
                else:
                    if response[1]==firstCard[1]:
                        if Cards.getRank(response)["value"]>Cards.getRank(firstCard)["value"] and\
                            Cards.getRank(response)["value"]>Cards.getRank(secondCard)["value"]:
                            return True
                        else:
                            for card in remaining:
                                if card[1]==firstCard[1]:
                                    if Cards.getRank(card)["value"]>Cards.getRank(firstCard)["value"] and\
                                        Cards.getRank(card)["value"]>Cards.getRank(secondCard)["value"]:
                                        return False
                            return True
                    elif response[1]=="S":
                        for card in remaining:
                            if card[1]==firstCard[1]:
                                return False
                        return True
                    else:
                        for card in remaining:
                            if card[1]==firstCard[1] or card[1]=="S":
                                return False
                        return True
            elif secondCard[1]=="S":
                if thirdCard[1]==firstCard[1]:
                    if response[1]==firstCard[1]:
                        return True
                    elif response[1]=="S":
                        for card in remaining:
                            if card[1]==firstCard[1]:
                                return False
                        if Cards.getRank(response)["value"]>Cards.getRank(secondCard)["value"]:
                            return True
                        else:
                            for card in remaining:
                                if card[1]=="S":
                                    if Cards.getRank(card)["value"]>Cards.getRank(secondCard)["value"]:
                                        return False
                            return True
                    else:
                        for card in remaining:
                            if card[1]==firstCard[1]:
                                return False
                            elif card[1]=="S":
                                if Cards.getRank(card)["value"]>Cards.getRank(secondCard)["value"]:
                                    return False
                        return True
                elif thirdCard[1]=="S":
                    if response[1]==firstCard[1]:
                        return True
                    elif response[1]=="S":
                        for card in remaining:
                            if card[1]==firstCard[1]:
                                return False
                        if Cards.getRank(response)["value"]>Cards.getRank(thirdCard)["value"] and\
                            Cards.getRank(response)["value"]>Cards.getRank(secondCard)["value"]:
                            # print("greater than both")
                            return True
                        else:
                            for card in remaining:
                                if card[1]=="S":
                                    if Cards.getRank(card)["value"]>Cards.getRank(thirdCard)["value"] and\
                                        Cards.getRank(card)["value"]>Cards.getRank(secondCard)["value"]:
                                        return False
                            return True 
                    else:
                        for card in remaining:
                            if card[1]==firstCard[1]:
                                return False
                            elif card[1]=="S":
                                if Cards.getRank(card)["value"]>Cards.getRank(secondCard)["value"]\
                                    and Cards.getRank(card)["value"]>Cards.getRank(thirdCard)["value"]:
                                    return False
                        return True
                else:
                    if response[1]==firstCard[1]:
                        return True
                    elif response[1]=="S":
                        for card in remaining:
                            if card[1]==firstCard[1]:
                                return False
                        if Cards.getRank(response)["value"]>Cards.getRank(secondCard)["value"]:
                            return True
                        else:
                            for card in remaining:
                                if card[1]=="S":
                                    if Cards.getRank(card)["value"]>Cards.getRank(secondCard)["value"]:
                                        return False
                            return True 
                    else:
                        for card in remaining:
                            if card[1]==firstCard[1]:
                                return False
                            elif card[1]=="S":
                                if Cards.getRank(card)["value"]>Cards.getRank(secondCard)["value"]:
                                    return False
                        return True
            else:
                if thirdCard[1]==firstCard[1]:
                    if response[1]==firstCard[1]:
                        if Cards.getRank(response)["value"]>Cards.getRank(firstCard)["value"] and\
                            Cards.getRank(response)["value"]>Cards.getRank(thirdCard)["value"]:
                            return True
                        else:
                            for card in remaining:
                                if card[1]==firstCard[1]:
                                    if Cards.getRank(card)["value"]>Cards.getRank(firstCard)["value"] and\
                                        Cards.getRank(card)["value"]>Cards.getRank(thirdCard)["value"]:
                                        return False
                            return True
                    elif response[1]=="S":
                        for card in remaining:
                            if card[1]==firstCard[1]:
                                return False
                        return True
                    else:
                        for card in remaining:
                            if card[1]=="S" or card[1]==firstCard[1]:
                                return False
                        return True
                elif thirdCard[1]=="S":
                    if response[1]==firstCard[1]:
                        return True
                    elif response[1]=="S":
                        for card in remaining:
                            if card[1]==firstCard[1]:
                                return False
                        if Cards.getRank(response)["value"]>Cards.getRank(thirdCard)["value"]:
                            return True
                        else:
                            for card in remaining:
                                if card[1]=="S":
                                    if Cards.getRank(response)["value"]>Cards.getRank(thirdCard)["value"]:
                                        return False
                            return True
                    else:
                        for card in remaining:
                            if card[1]==firstCard[1]:
                                return False
                            elif card[1]=="S":
                                if Cards.getRank(card)["value"]>Cards.getRank(thirdCard)["value"]:
                                    return False
                        return True
                else:
                    if response[1]==firstCard[1]:
                        if Cards.getRank(response)["value"]>Cards.getRank(firstCard)["value"]:
                            return True
                        else:
                            for card in remaining:
                                if card[1]==firstCard[1]:
                                    if Cards.getRank(card)["value"]>Cards.getRank(firstCard)["value"]:
                                        return False
                            return True
                    elif response[1]=="S":
                        for card in remaining:
                            if card[1]==firstCard[1]:
                                return False
                        return True
                    else:
                        for card in remaining:
                            if card[1]==firstCard[1] or card[1]=="S":
                                return False
                        return True

    @staticmethod
    def check8HandWin(players):#this function has not been used currently
        for player in players:
            if player.scores[GameMaster.round-1]==8:
                player.R=1000
                player.totalR+=player.R0
                return True
        return False
    
    @staticmethod
    def check3HandExact(players):#this function has not been used
        #this is called if the third round of the game is completed
        #thee rule however needs to ve verified from BHoos!
        flag=[False, False, False, False]
        for player in players:
            for i in range(3):
                pass

    #reward funcitons are stored over here
    @staticmethod
    def roundWinReward(player):#this function has not been used
        # print("the round win reward was obtained by player "+ player.playerName)
        player.R+=10

    @staticmethod
    def gameWinReward(player):#this function has not been used
        # print("the game win reward was obtained by player "+ player.playerName)
        player.R+=100

    @staticmethod
    def plotExpectedRewards(players, save = False):
        plt.figure(figsize=(10,12))
        legend=[]
        for i,player in enumerate(players):
            plt.plot(player.historyOfQ)
            #this prints the player name, epsilon, alpha and gamma of the players
            legend.append(player.playerName+f" ,e={player.epsilon}, a={player.alpha}, g={player.gamma}")
        plt.legend(legend)
        plt.title("Expected Rewards")    
        plt.show()
        if save:
            plt.savefig("expectedQ.png")
    
        
        
                        




