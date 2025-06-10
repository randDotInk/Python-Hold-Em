# aggressive_bot.py
import random
import PokerMoves as PM

def turn(stage, amount, betList, turn, hand, comCards, bank, pot):
    strength = PM.evaluateHand(hand + comCards)

    if stage == 1:
        # Ante stage: always match or raise slightly
        if bank <= amount:
            return PM.check(amount, betList, turn, bank, pot)
        raise_amt = min(bank, amount + random.randint(1, 5))
        if random.random() < 0.5:
            return PM.raiseTo(raise_amt, amount, betList, turn, bank, pot)
        else:
            return PM.check(amount,betList,turn,bank,pot)


    if stage == 2:
        if strength >= 6:
            return PM.raiseTo(min(bank, amount + random.randint(20, 40)), amount, betList, turn, bank, pot)
        elif strength >= 3:
            if random.random() < 0.7:
                return PM.raiseTo(min(bank, amount + random.randint(10, 25)), amount, betList, turn, bank, pot)
            else:
                return PM.check(amount, betList, turn, bank, pot)
        else:
            if random.random() < 0.3:
                return PM.raiseTo(min(bank, amount + random.randint(5, 10)), amount, betList, turn, bank, pot)
            return PM.check(amount, betList, turn, bank, pot)
