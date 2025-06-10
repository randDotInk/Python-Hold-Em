# random_bot.py
import random
import PokerMoves as PM

def turn(stage, amount, betList, turn, hand, comCards, bank, pot):
    if stage == 1:
        # Ante stage: randomly fold or call or raise small
        r = random.random()
        if r < 0.2 and amount > 0:
            return PM.fold(amount, betList, turn, bank, pot)
        elif r < 0.6:
            return PM.check(amount, betList, turn, bank, pot)
        else:
            return PM.raiseTo(min(bank, amount + random.randint(1, 5)), amount, betList, turn, bank, pot)

    if stage == 2:
        action = random.choice(['raise', 'check', 'fold', 'allin'])
        if action == 'raise':
            return PM.raiseTo(min(bank, amount + random.randint(5, 30)), amount, betList, turn, bank, pot)
        elif action == 'check':
            return PM.check(amount, betList, turn, bank, pot)
        elif action == 'fold':
            return PM.fold(amount, betList, turn, bank, pot)
        else:
            return PM.allIn(amount, betList, turn, bank, pot)
