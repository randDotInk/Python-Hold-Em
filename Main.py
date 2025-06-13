import PokerMoves as pm
import random
import passive_bot
import aggressive_bot
import random_bot

def all_active_players_matched_bet(status_list, current_bet):
    return all(p[0] in [-3, -4] or p[1] == current_bet for p in status_list)

# --- Setup deck ---
faces = ["S", "H", "D", "C"]
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', "J", "Q", "K", 'A']

# --- Players ---
players = dict(DL=2000, RC=2000, MU=2000, LH=2000, SK=2000, JP=2000, JC=2000, CS=2000, JK=2000)
player_keys = list(players.keys())
playerStatus = [[0, 0, 2000, 0] for _ in player_keys]

# --- Set bots ---
bot_map = {
    "DL": passive_bot,
    "RC": aggressive_bot,
    "MU": passive_bot,
    "LH": passive_bot,
    "SK": random_bot,
    "JP": passive_bot,
    "JC": aggressive_bot,
    "CS": aggressive_bot,
    "JK": aggressive_bot
}

for k in range(90):
    print(f"\n=== ROUND {k + 1} ===")

    starting_stacks = {key: players[key] for key in player_keys}
    playerStatus = [[0, 0, players[key], 0] for key in player_keys]

    deck = [(face, rank) for rank in ranks for face in faces]
    random.shuffle(deck)
    betList = [0] * len(players)
    hands = {key: [deck.pop(0), deck.pop(0)] for key in player_keys}
    Community = []
    pot = 0
    ante = 1
    bet = 0

    # --- Ante Round ---
    while not (all(p[1] == ante or p[0] in [-3, -4] for p in playerStatus) and sum(betList) > 0):
        for i, key in enumerate(player_keys):
            if all(p[1] == ante or p[0] in [-3, -4] for p in playerStatus) and sum(betList) > 0:
                break
            if playerStatus[i][0] in [-3, -4]:
                continue

            bot_instance = bot_map[key]
            playerStatus[i] = bot_instance.turn(1, ante, betList, i, hands[key], Community, players.values(),
                                                playerStatus[i][2], pot)
            ante = max(ante, playerStatus[i][1])
            players[key] = playerStatus[i][2]
            pot = max(pot, playerStatus[i][3])
            betList[i] = ante

    print("ANTE OVER")
    print(f"Ante: {ante}")
    print(f"Chip counts: {players}")

    # --- Deal Flop ---
    Community = [deck.pop(0), deck.pop(0), deck.pop(0)]
    print("Flop:", Community)

    # --- Betting Rounds (Turn + River) ---
    for _ in range(2):
        bet = 0
        for i in range(len(betList)):
            if playerStatus[i][0] in [-1, -2]:
                playerStatus[i][0] = 0
                betList[i] = 0
            playerStatus[i][1] = 0

        while not all_active_players_matched_bet(playerStatus, bet):
            for i, key in enumerate(player_keys):
                if all_active_players_matched_bet(playerStatus, bet):
                    break
                if playerStatus[i][0] in [-3, -4]:
                    playerStatus[i][1] = bet
                    continue

                bot_instance = bot_map[key]
                playerStatus[i] = bot_instance.turn(2, bet, betList, i, hands[key], Community, players.values(),playerStatus[i][2], pot)

                bet = max(bet, playerStatus[i][1])
                players[key] = playerStatus[i][2]
                pot = max(pot, playerStatus[i][3])
                betList[i] = playerStatus[i][1]
                print(f"DEBUG: {key} status = {playerStatus[i]}")


        Community.append(deck.pop(0))
        print("Community cards:", Community)

    # --- Evaluate Scores ---
    final_scores = []
    for i, key in enumerate(player_keys):
        if playerStatus[i][0] == -3:
            final_scores.append((key, -1))
        else:
            final_scores.append((key, pm.evaluateHand(hands[key] + Community)))
    final_scores.sort(key=lambda x: x[1], reverse=True)
    print("Scores:", final_scores)
    print("\nPlayers still in the hand and their cards:")
    for i, key in enumerate(player_keys):
        if playerStatus[i][0] != -3:  # Not folded
            hand_cards = hands[key]
            # Format nicely as "RankSuit"
            formatted_hand = [f"{rank}{suit}" for suit, rank in hand_cards]
            print(f"{key}: {formatted_hand}")

    # --- Build Contribution List ---
    contributions = {key: starting_stacks[key] - players[key] for key in player_keys}

    # --- Build Side Pots ---
    side_pots = []
    sorted_contribs = sorted(set(contributions.values()))
    previous = 0
    for threshold in sorted_contribs:
        eligible = [key for key in player_keys if contributions[key] >= threshold]
        pot_amount = (threshold - previous) * len(eligible)
        if pot_amount > 0:
            side_pots.append((eligible.copy(), pot_amount))
        previous = threshold

    # --- Distribute Side Pots (Correctly) ---
    pot_distributed = 0
    for eligible, side_amount in side_pots:
        top_score = -1
        side_winners = []
        for name, score in final_scores:
            if name not in eligible:
                continue
            if score > top_score:
                top_score = score
                side_winners = [name]
            elif score == top_score:
                side_winners.append(name)

        if side_winners:
            share = side_amount // len(side_winners)
            distributed = share * len(side_winners)
            leftover = side_amount - distributed
            for winner in side_winners:
                players[winner] += share
            if leftover > 0:
                players[side_winners[0]] += leftover
            pot_distributed += side_amount

    # --- Final leftover cleanup ---
    leftover = max(0, pot - pot_distributed)
    if leftover > 0 and final_scores:
        players[final_scores[0][0]] += leftover

    # --- Sanity check ---
    total_before = sum(starting_stacks.values())
    total_after = sum(players.values())
    assert total_before == total_after, f"Money mismatch! Before: {total_before}, After: {total_after}"

    print(f"Final chip counts: {players}")

    # --- Remove busted players (careful index removal) ---
    to_remove = [i for i, status in enumerate(playerStatus) if status[2] <= 0]
    for i in reversed(to_remove):
        key = player_keys[i]
        print(f"Bye bye {key}")
        key = player_keys[i]
        playerStatus.pop(i)
        player_keys.pop(i)
        players.pop(key)

    if len(player_keys) == 1:
        print(f"Final Winner is {player_keys[0]} with ${players[player_keys[0]]}")
        break

    # --- Rotate player order ---
    players = list(players.items())
    res = [players[(i - 1) % len(players)] for i in range(len(players))]
    players = {k: v for k, v in res}
    player_keys = player_keys[-1:] + player_keys[:-1]
    playerStatus = playerStatus[-1:] + playerStatus[:-1]

    input("Press Enter for next round...")

# --- Game Over ---
if len(player_keys) != 1:
    max_chips = max(players.values())
    winner = [k for k, v in players.items() if v == max_chips][0]
    print(f"Final winner is {winner} with ${players[winner]}")
