import random
import numpy as np
import time


SUITS = ["H", "D", "C", "S"]
NUMBERS = np.array(["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"])

def cardToNumber(card):
    return int(np.where(NUMBERS == card[:-1])[0]) + SUITS.index(card[-1]) * 13

def numberToCard(num):
    return NUMBERS[num % 13] + SUITS[num // 13]

nFunc = np.vectorize(numberToCard)

def getHandStrength(cards):
    cards = np.array(cards)
    
    ranks, counts = np.unique(cards % 13, return_counts=True)
    suits, sCounts = np.unique(cards // 13, return_counts=True)
    # for i in cards:
    #     print(numberToCard(i))
    
    # straight flush
    for i in range(4):
        for j in range(8, -1, -1):
            flag = True
            for k in range(5):
                if i * 13 + j + k not in cards:
                    flag = False
                    break
            if flag:
                # print(f"Straight Flush starting at {NUMBERS[j]}")
                return 10 ** 20 + j
            
    for i in range(4):
        if i * 13 + 12 in cards:
            flag = True
            for j in range(4):
                if i * 13 + j not in cards:
                    flag = False
                    break
            if flag:
                # print("Straight Flush starting at Ace")
                return 10 ** 20 - 1
    
    # four of a kind
    if 4 in counts:
        value = int(ranks[np.where(counts == 4)[0]])
        kicker = int(ranks[np.where(ranks != value)].max())
        # print(f"Quads ({NUMBERS[int(value)]}) with {NUMBERS[kicker]} kicker")
        return 10 ** 19 + value * 10000 + kicker
    
    # full house
    if np.sort(counts)[-2] == 3:
        large = int(ranks[np.where(counts == 3)].max())
        lil = int(ranks[np.where(counts == 3)].min())
        # print(f"{NUMBERS[large]} full of {NUMBERS[lil]}")
        return 10 ** 18 + large * 100 + lil
    
    if 3 in counts and 2 in counts:
        large = int(ranks[np.where(counts == 3)[0]])
        lil = int(ranks[np.where(counts == 2)].max())
        # print(f"{NUMBERS[large]} full of {NUMBERS[lil]}")
        return 10 ** 18 + large * 100 + lil

    
    # flush
    if sCounts.max() >= 5:
        flush_suit = int(suits[np.where(sCounts >= 5)][0])
        flush_cards = cards[np.where(cards // 13 == flush_suit)]
        flush_ranks = flush_cards % 13
        top5 = np.sort(flush_ranks)[-5:]
        # print(f"Flush of {NUMBERS[top5]}")
        return 10**17 + sum(val * (100**i) for i, val in enumerate(top5))

    # straight
    for i in range(8, -1, -1):
        flag = True
        for j in range(5):
            if i + j not in ranks:
                flag = False
                break
        if flag:
            # print(f"Straight starting at {NUMBERS[i]}")
            return 10 ** 16 + i
    if 12 in ranks:
        flag = True
        for i in range(4):
            if i not in ranks:
                flag = False
                break
        if flag:
            # print("Straight starting at A")
            return 10 ** 16 - 1
    
    # three of a kind
    if 3 in counts:
        large = int(ranks[np.where(counts == 3)[0]])
        kickers = np.sort(ranks[np.where(ranks != large)])[-2:]
        # print(f"Three of a kind ({NUMBERS[large]}) with kickers {NUMBERS[kickers[-1]]} and {NUMBERS[kickers[-2]]}")
        return 10 ** 15 + large * 10 ** 4 + kickers[-1] * 10 ** 2 + kickers[-2]

    # two pair
    if np.sort(counts)[-2] == 2:
        pairs = np.sort(ranks[np.where(counts == 2)])[-2:]
        kicker = max(rank for rank in ranks if rank not in pairs)
        # print(f"Two Pair ({pairs[1]} and {pairs[0]}) with kicker {kicker}")
        
        # print(nFunc(cards))
        # print(pairs)
        return 10 ** 14 + pairs[1] * 10 ** 4 + pairs[0] * 10 ** 2 + kicker
    
    if np.sort(counts)[-1] == 2:
        pair = np.sort(ranks[np.where(counts == 2)])[-1]
        kickers = np.sort(ranks[np.where(ranks != pair)])[-3:]
        # print(f"Pair ({pair}) with kickers {kickers}")
        kickers = np.append(kickers, pair)
        return 10 ** 13 + sum(val * (100**i) for i, val in enumerate(kickers))
    
    kickers = np.sort(ranks)[-5:]
    # print(f"High Card {np.sort(ranks)[-5:]}")
    return 10 ** 12 + sum(val * (100**i) for i, val in enumerate(kickers))
    

class Board():
    def __init__(self, hand, board = [], players = 1):
        self.hand = hand
        self.players = players
        self.kboard = board
        self.usedCards = hand + board
        
    
    def compare(self):
        p1 = getHandStrength(self.hand + self.board)
        others = []
        for i in self.others:
            others.append(getHandStrength(i + self.board))
        if p1 == max(others):
            return -1
        return p1 > max(others)
    
    def fillBoard(self, deadCard = []):
        self.board = self.kboard.copy()
        while len(self.board) < 5:
            card = random.randint(0, 51)
            if card not in self.tUsedCards:
                self.tUsedCards.append(card)
                self.board.append(card)
                
    def fillOpps(self):
        self.others = []
        for i in range(self.players):
            self.others.append([])
            while len(self.others[-1]) < 2:
                card = random.randint(0, 51)
                if card not in self.tUsedCards:
                    self.others[-1].append(card)
                    self.tUsedCards.append(card)

    def runSimOnce(self):
        self.fillOpps()
        self.fillBoard()
        return self.compare()
    
    # def fillOppK(self, hand):
    #     self.p2 = hand
    
    def simpleRunSim(self, counter = 10 ** 5):
        win = 0
        lose = 0
        tie = 0
        for i in range(counter):
            self.tUsedCards = self.usedCards.copy()
            # print(i)
            output = self.runSimOnce()
            if output == -1:
                tie += 1
            elif output:
                win += 1
            else:
                lose += 1
        return {
            "win": round(win / counter, 4),
            "lose": round(lose / counter, 4),
            "tie": round(tie / counter, 4)
        }
    
    
    
    def doAll(self, simCount = 10 ** 5):
        win = 0
        lose = 0
        tie = 0
        
        for counter in range(simCount):
            self.tUsedCards = self.usedCards.copy()
            
            
            self.others = []
            for j in range(self.players):
                self.others.append([])
                while len(self.others[-1]) < 2:
                    card = random.randint(0, 51)
                    if card not in self.tUsedCards:
                        self.others[-1].append(card)
                        self.tUsedCards.append(card)
                        
            self.board = self.kboard.copy()
            while len(self.board) < 5:
                card = random.randint(0, 51)
                if card not in self.tUsedCards:
                    self.tUsedCards.append(card)
                    self.board.append(card)
            
            # print(counter)
            
            p1 = getHandStrength(self.hand + self.board)
            others = []
            for j in self.others:
                others.append(getHandStrength(j + self.board))
            if p1 == max(others):
                tie += 1
            elif p1 > max(others):
                win += 1
            else:
                lose += 1
        return {
            "win": round(win / counter, 4),
            "lose": round(lose / counter, 4),
            "tie": round(tie / counter, 4)
        }
            

    

def calculate_odds(hand, board = []):
    """
    Dummy placeholder for now.
    'hand' and 'board' are lists of strings like ["AS", "KH"]
    """
    print(hand)
    print(board)
    for i in range(len(hand)):
        if type(hand[i]) == str:
            hand[i] = cardToNumber(hand[i])
    for i in range(len(board)):
        if type(board[i]) == str:
            board[i] = cardToNumber(board[i])
    board = Board(hand, board, players = 1)
    return board.doAll(10 ** 4)
    

# print(calculate_odds([12, 25]))
