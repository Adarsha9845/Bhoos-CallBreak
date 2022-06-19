SUIT = {
    "HEART": {"value": 2, "code": "H"},
    "CLUB": {"value": 3, "code": "C"},
    "DIAMOND": {"value": 4, "code": "D"},
    # spade always trumps other cards
    "SPADE": {"value": 1, "code": "S"},
    "NONE":{"value": 0, "code": "N"}
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
    "NONE": {"value": 0, "code": "N"},
}

class Cards:
    suit = 'HCDS'
    val = '123456789TJQK'

    @staticmethod
    def createCombo():
        return [x+y for x in Cards.val for y in Cards.suit]
    
    @staticmethod
    def getRank(card):
        if card==None:
            return RANK["NONE"]
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

    @staticmethod
    def getSuit(card: str):
        if card==None:
            return SUIT["NONE"]
        if card[1] == "H":
            return SUIT["HEART"]
        elif card[1] == "C":
            return SUIT["CLUB"]
        elif card[1] == "D":
            return SUIT["DIAMOND"]
        elif card[1] == "S":
            return SUIT["SPADE"]
        
    # def __str__(self) -> str:
    #     return self.rank["code"] + self.suit["code"]