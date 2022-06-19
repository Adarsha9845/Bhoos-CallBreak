from cards import Cards
from gameMaster import GameMaster
cardz=['2S', '5C', '4H','9C']
played=['KD','3D','5S']

firstCard=0
playedSpade=[]
diamond=[]
heart=[]
club=[]
spade=[]

playable=[]

firstCard=played[0]
for card in played[1:]:
    if card[1]=="S":
        playedSpade.append(card)

def returnSuitCards(suit):
    if suit=="S":
        return spade
    elif suit=="H":
        return heart
    elif suit=="D":
        return diamond
    else:
        return club    

for card in cardz:
    if card[1]=="S":
        spade.append(card)
    elif card[1]=="H":
        heart.append(card)
    elif card[1]=="C":
        club.append(card)
    else:
        diamond.append(card)

if len(played)==0:
    playable=cardz
elif len(played)==1:
    temp=returnSuitCards(firstCard[1])
    if len(temp)!=0:
        for card in temp:
            if Cards.getRank(card)["value"]>Cards.getRank(firstCard)["value"]:
                playable.append(card)
        if len(playable)==0:
            playable=temp
    else:
        playable=returnSuitCards('S')
        if len(playable)==0:
            playable=cardz        
elif len(played)==2:
    secondCard=played[1]
    temp=returnSuitCards(firstCard[1])
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
        temp=returnSuitCards('S')
        if secondCard[1]=="S":
            for card in temp:
                if Cards.getRank(card)["value"]>Cards.getRank(secondCard)["value"]:
                    playable.append(card)
            if len(playable)==0:
                playable=cardz
        else:
            playable=returnSuitCards('S')
        if len(playable)==0:
            playable=cardz
else:
    secondCard=played[1]
    thirdCard=played[2]
    temp=returnSuitCards(firstCard[1])
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
        temp=returnSuitCards('S')
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
                playable=cardz
        else:
            if len(temp)==0:
                playable=cardz



print(playable)

