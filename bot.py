import PokerMoves as PM
import random

def turn(stage, amount, betList, turn, hand, comCards, bank, pot):
    hand_strength = PM.evaluateHand(hand + comCards)
    bet = 0

    if stage == 1:
        # Early game randomizer
        if bank <= amount or amount > bank // 4:
            return PM.fold(amount, betList, turn, bank, pot)
        bet = random.randint(amount, min(bank, amount + 20))
        return PM.raiseTo(bet, amount, betList, turn, bank, pot)

    if stage == 2:
        # Better logic post-flop
        if hand_strength >= 7:  # Four of a kind or better
            bet = min(bank, amount + random.randint(20, 50))
            return PM.raiseTo(bet, amount, betList, turn, bank, pot)
        elif hand_strength >= 5:  # Flush or full house
            bet = min(bank, amount + random.randint(10, 25))
            return PM.raiseTo(bet, amount, betList, turn, bank, pot)
        elif hand_strength >= 3:  # 3 of a kind or straight
            if amount <= bank // 4:
                return PM.check(amount, betList, turn, bank, pot)
            else:
                return PM.fold(amount, betList, turn, bank, pot)
        else:
            # Weak hand
            if amount > bank // 6:
                return PM.fold(amount, betList, turn, bank, pot)
            else:
                return PM.check(amount, betList, turn, bank, pot)
