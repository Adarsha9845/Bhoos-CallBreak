import numpy as np

# playInfo = {
#         "timeBudget": None,  # float
#         "playerId": None,  # string
#         # 4 strings
#         "playerIds": [
#             "P0",
#             "P1",
#             "P2",
#             "P3"
#         ],
#         #  upto 13 cards in string format
#         "cards": [],
#         #  upto 3 cards in order from last winner
#         #  last winner can be inferred from last item in history
#         #  e.g > payload.history[payload.history.length - 1][2]
#         "played": [],
#         #  'history' field contains an ordered list of cards played from first hand.
#         #  Format: 'start idx, [cards in clockwise order of player ids], winner idx'
#         #  'start idx' is index of player that threw card first
#         #  'winner idx' is index of player who won this hand
#         "history": [],
#         #  Context has metadata about the current round:
#         #  'ruond': the current round[1 - 5]
#         #  'totalPoints': the points accumulated till this round(dhoos is also subtracted)
#         #  'bid': bid of current round
#         #  'won': total hands won this round upto this point
#         "context": {
#             "round": 0,
#             "players": {
#                 "P0": {
#                     "totalPoints": 0,
#                     "bid": 0,
#                     "won": 0
#                 },
#                 "P1": {
#                     "totalPoints": 0,
#                     "bid": 0,
#                     "won": 0
#                 },
#                 "P2": {
#                     "totalPoints": 0,
#                     "bid": 0,
#                     "won": 0
#                 },
#                 "P3": {
#                     "totalPoints": 0,
#                     "bid":0,
#                     "won":0
#                 }
#             }
#         }
#     }

SUIT = {
    "HEART": {"value": 2, "code": "H"},
    "CLUB": {"value": 3, "code": "C"},
    "DIAMOND": {"value": 4, "code": "D"},
    # spade always trumps other cards
    "SPADE": {"value": 1, "code": "S"},
}


RANK = {
    "TWO": {"value": 2, "code": "2"},
    "THREE": {"value": 3, "code": "3"},
    "FOUR": {"value": 4, "code": "4"},
    "FIVE": {"value": 5, "code": "5"},
    "SIX": {"value": 6, "code": "6"},
    "SEVEN": {"value": 7, "code": "7"},
    "EIGHT": {"value": 8, "code": "8"},
    "NINE": {"value": 9, "code": "9"},
    "TEN": {"value": 10, "code": "T"},
    "JACK": {"value": 11, "code": "J"},
    "QUEEN": {"value": 12, "code": "Q"},
    "KING": {"value": 13, "code": "K"},
    "ACE": {"value": 14, "code": "1"},
}

def getRank(card):
        if card[0] == "2":
            return RANK["TWO"]
        if card[0] == "3":
            return RANK["THREE"]
        if card[0] == "4":
            return RANK["FOUR"]
        if card[0] == "5":
            return RANK["FIVE"]
        if card[0] == "6":
            return RANK["SIX"]
        if card[0] == "7":
            return RANK["SEVEN"]
        if card[0] == "8":
            return RANK["EIGHT"]
        if card[0] == "9":
            return RANK["NINE"]
        if card[0] == "T":
            return RANK["TEN"]
        if card[0] == "J":
            return RANK["JACK"]
        if card[0] == "Q":
            return RANK["QUEEN"]
        if card[0] == "K":
            return RANK["KING"]
        # Ace is always the highest value card
        if card[0] == "1":
            return RANK["ACE"]


def getSuit(card: str):
        if card[1] == "H":
            return SUIT["HEART"]
        if card[1] == "C":
            return SUIT["CLUB"]
        if card[1] == "D":
            return SUIT["DIAMOND"]
        if card[1] == "S":
            return SUIT["SPADE"]

def my_card_encoding(cards):

    my_card = [0] * 26
    counter = 0
    for card in cards:
        my_card[counter] = getRank(card)['value']
        counter = counter + 1
        my_card[counter] = getSuit(card)['value']
        counter = counter + 1

    return my_card
        




def played_card_Func(played):
    played_card = [0] * 8
    counter = 0
    for card in played:
        played_card[counter] = getRank(card)['value']
        counter = counter + 1
        played_card[counter] = getSuit(card)['value']
        counter = counter + 1
    return played_card


def largestSmallestNumFunc(historys):
    
    remainingcard = [0] * 8
    counter = 0
    # for history in historys:
    #     for card in history[1]:
    return remainingcard


def possibleMoveEnc(possibleMove):
    encod_possible = [0] * 2
    encod_possible[0] = getRank(possibleMove)['value']
    encod_possible[1] = getSuit(possibleMove)['value']
    return encod_possible















            
print(my_card_encoding(['1S', 'KS', '5D']))




# Possible_move is a possible card suggested..
def input_encoding(playInfo, possible_move):

    # remaining card in the hand..
    my_card = my_card_encoding(playInfo['cards'])

    # played card in the order..
    played_card = played_card_Func = (playInfo['played'])

    #Largest and Smallest number of card than ours largest card..

    largestSmallestNum = largestSmallestNumFunc(playInfo['history'], playInfo['cards'])
    
    possibleMove = possibleMoveEnc(possible_move)

    finalInputEncoding = []
    finalInputEncoding = finalInputEncoding.append(my_card)
    finalInputEncoding = finalInputEncoding.append(played_card)
    finalInputEncoding = finalInputEncoding.append(largestSmallestNum)
    finalInputEncoding = finalInputEncoding.append(possibleMove)

    return finalInputEncoding




