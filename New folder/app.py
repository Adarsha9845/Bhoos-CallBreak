from gameMaster import GameMaster

from player import Player
from cards import Cards
from network import Network
import numpy as np

players=[Player() for _ in range(4)]
for aa in range(1000):
    for a in range(5):
        GameMaster.round+=1
        print("Round %d\n"%GameMaster.round)
        for player, card in zip(players,GameMaster.distribute()):
            print(card)
            player.dealtCards(card)
        # print("The cards have been dealt::::")
        # print("Here we come to bidding phase")
        GameMaster.biddingPhase(players,riskFactor=1)
        # print("The bid info is here")
        # print(GameMaster.bidInfo)
        # print("##############")
        # print("Starting of round")
        GameMaster.oneRound(players)
    # if aa==999:
    #     #to display the scores at the last iteration fo 1000 games
    #     print(GameMaster.playInfo)
    GameMaster.resetGameMaster()
    #We need to reset the players after each round
    #variables such as weights and totalWins remain same and don't reset
    for player in players:
        player.resetPlayer(aa)
GameMaster.plotExpectedRewards(players, save = True)
for player in players:
        print(f"Total wins of player {player.playerName} is {player.totalWins}")
