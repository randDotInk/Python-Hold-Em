# passive_bot.py
import random
import PokerMoves as PM

def turn(stage, amount, betList, turn, hand, comCards, bank, pot):
    strength = PM.evaluateHand(hand + comCards)

    if stage == 1:
        # Ante stage: just call or fold
        if bank < amount:
            return PM.fold(amount, betList, turn, bank, pot)
        return PM.check(amount, betList, turn, bank, pot)

    if stage == 2:
        if strength >= 7:
            return PM.raiseTo(min(bank, amount + 10), amount, betList, turn, bank, pot)
        elif strength >= 4:
            return PM.check(amount, betList, turn, bank, pot)
        else:
            if amount == 0:
                return PM.check(amount, betList, turn, bank, pot)
            else:
                return PM.fold(amount, betList, turn, bank, pot)
