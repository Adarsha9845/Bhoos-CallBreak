from gameMaster import GameMaster

from player import Player

players=[Player(epsilon=0) for _ in range(4)]
for player in players:
    player.readWeightsNBiases(player="P2")
 

for _ in range(5):
    GameMaster.round+=1
    print("Round %d:\n"%GameMaster.round)
    for player, card in zip(players,GameMaster.distribute()):
        print(card)
        player.dealtCards(card)
    # print("Here we come to bidding phase")
    GameMaster.biddingPhase(players,printBidInfo=True,riskFactor=0)
    # starting the round
    GameMaster.oneRound(players,printHistory=True,train=False)
    
print(players[0].network.weights)