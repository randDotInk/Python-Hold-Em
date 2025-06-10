handorder = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

def raiseTo(bet, Amount, betList, turn, bank, pot):
    prevCall = betList[turn]
    if bet < Amount:
        bet = Amount
    if bet == 0:
        return [-1, 0, bank, pot]  # Check or call

    if bet < 0:
        return [-3, Amount, bank, pot]  # Fold

    extra = bet - prevCall  # Additional amount needed to put in

    if bank < extra:
        # Player goes all in with remaining bank
        pot += bank
        bank = 0
        return [-4, bet, bank, pot]

    bank -= extra
    pot += extra

    if bet > Amount:
        return [-2, bet, bank, pot]  # Raise
    else:
        return [-1, bet, bank, pot]  # Call


def raiseBy(bet, Amount, betList, turn, bank, pot):
    prevCall = betList[turn]
    if bet < Amount:
        bet = Amount
    if bet == 0:
        return [-1, 0, bank, pot]

    if bet < 0:
        return [-3, Amount, bank, pot]

    extra = bet - prevCall

    if bank < extra:
        pot += bank
        bank = 0
        return [-4, bet, bank, pot]

    bank -= extra
    pot += extra

    if bet > Amount:
        return [-2, bet, bank, pot]
    else:
        return [-1, bet, bank, pot]


def check(Amount, betList, turn, bank, pot):
    prevCall = betList[turn]
    if Amount == 0:
        # Player checks
        return [-1, 0, bank, pot]

    if bank < Amount:
        # Player cannot cover call, goes all in
        pot += bank
        bank = 0
        return [-4, Amount, bank, pot]

    bank -= Amount
    pot += Amount
    return [-1, Amount, bank, pot]


def fold(Amount, betList, turn, bank, pot):
    return [-3, Amount, bank, pot]


def allIn(Amount, betList, turn, bank, pot):
    if bank <= 0:
        return [-3, 0, bank, pot]
    pot += bank
    bank = 0
    return [-4, Amount, bank, pot]


def handrank(hand):
    hand = sortByHighest(hand)
    isSeq = isSequential(hand)
    isSuit = isSameSuit(hand)
    dupes = getMostDups(hand)
    total = 0.0
    highest = getHighestCard(hand)

    if isSeq and isSuit:
        royal = ["10", "J", "Q", "K", "A"]
        top_ranks = [card[1] for card in hand[:5]]
        if all(rank in top_ranks for rank in royal):
            return 9.0
        total = 8.0 + highest / 100
        return total

    elif dupes[0] == 4:
        total = 7.0 + handorder.index(dupes[1]) / 100
        if hand[0][1] != dupes[1]:
            total += handorder.index(hand[0][1]) / 10000
        else:
            total += handorder.index(hand[4][1]) / 10000
        return total

    elif dupes[0] == 3:
        fhflag = True
        if hand[0][1] == dupes[1]:
            fhflag = (hand[0][1] == hand[1][1] == hand[2][1]) and (hand[3][1] == hand[4][1])
        else:
            fhflag = (hand[0][1] == hand[1][1]) and (hand[2][1] == hand[3][1] == hand[4][1])
        if fhflag:
            total = 6.0
        else:
            total = 3.0
        total += handorder.index(dupes[1]) / 100.0
        return total

    elif isSuit:
        total = 5.0
        total += handorder.index(hand[0][1]) / 100.0
        total += handorder.index(hand[1][1]) / 10000.0
        total += handorder.index(hand[2][1]) / 1000000.0
        total += handorder.index(hand[3][1]) / 100000000.0
        total += handorder.index(hand[4][1]) / 10000000000.0
        return total

    elif isSeq:
        total = 4.0
        total += handorder.index(hand[0][1]) / 100.0
        return total

    elif dupes[0] == 2:
        tpflag = False
        tpdupe = ""
        for i in range(len(hand) - 1):
            if (hand[i][1] == hand[i + 1][1] and hand[i][1] != dupes[1]):
                tpflag = True
                tpdupe = hand[i][1]
        if tpflag:
            total = 2.0
            if handorder.index(dupes[1]) > handorder.index(tpdupe):
                total += handorder.index(dupes[1]) / 100
                total += handorder.index(tpdupe) / 10000
            else:
                total += handorder.index(tpdupe) / 100
                total += handorder.index(dupes[1]) / 10000
            for i in range(len(hand)):
                if hand[i][1] != dupes[1] and hand[i][1] != tpdupe:
                    total += handorder.index(hand[i][1]) / 1000000
                    break
            return total
        else:
            total = 1.0
            total += handorder.index(dupes[1]) / 100
            q = 10000.0
            for i in range(len(hand)):
                if hand[i][1] != dupes[1]:
                    total += handorder.index(hand[i][1]) / q
                    q *= 10.0
            return total

    total += handorder.index(hand[0][1]) / 100.0
    total += handorder.index(hand[1][1]) / 10000.0
    total += handorder.index(hand[2][1]) / 1000000.0
    total += handorder.index(hand[3][1]) / 100000000.0
    total += handorder.index(hand[4][1]) / 10000000000.0
    return total


def isSequential(hand):
    # Sort ascending by rank
    hand_sorted = sorted(hand, key=lambda c: handorder.index(c[1]))
    for i in range(1, len(hand_sorted)):
        if handorder.index(hand_sorted[i][1]) != handorder.index(hand_sorted[i - 1][1]) + 1:
            return False
    return True


def isSameSuit(hand):
    suit = hand[0][0]
    for i in range(1, len(hand)):
        if hand[i][0] != suit:
            return False
    return True


def getHighestCard(hand):
    highest = 0
    for card in hand:
        rank_index = handorder.index(card[1])
        if rank_index > highest:
            highest = rank_index
    return highest


def getMostDups(hand):
    mostDups = [0, "None"]
    for i in range(len(hand)):
        dupes = 0
        card = hand[i][1]
        for ii in range(i, len(hand)):
            if hand[ii][1] == card:
                dupes += 1
        if dupes > mostDups[0]:
            mostDups[0] = dupes
            mostDups[1] = card
    return mostDups


def sortByHighest(hand):
    newHand = []
    hand = hand[:]
    for _ in range(len(hand)):
        highest = ("C", "2")
        ri = 0
        for ii in range(len(hand)):
            if handorder.index(hand[ii][1]) > handorder.index(highest[1]):
                highest = hand[ii]
                ri = ii
        del hand[ri]
        newHand.append(highest)
    return newHand


def evaluateHand(seven_card_hand):
    best_score = 0.0
    for i in range(len(seven_card_hand)):
        for j in range(i + 1, len(seven_card_hand)):
            five_card_hand = []
            for k in range(len(seven_card_hand)):
                if k != i and k != j:
                    five_card_hand.append(seven_card_hand[k])
            score = handrank(five_card_hand)
            if score > best_score:
                best_score = score
    return best_score


