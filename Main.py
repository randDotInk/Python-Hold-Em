import PokerMoves as pm
import random
import passive_bot
import aggressive_bot
import random_bot# You only have one bot for now
def all_active_players_matched_bet(status_list, current_bet):
    return all(
        p[0] in [-3, -4] or p[1] == current_bet
        for p in status_list
    )
# --- Setup deck ---
faces = ["S", "H", "D", "C"]
ranks = ['2', '3', '4', '5', '6','7', '8', '9', '10', "J", "Q", "K",'A']
deck = [(face, rank) for rank in ranks for face in faces]
random.shuffle(deck)

# --- Players ---
players = dict(DL=2000, RC=2000, MU=2000, LH=2000, SK=2000, JP=2000, JC=2000, CS=2000)
player_keys = list(players.keys())
playerStatus = [[0, 0, 2000, 0] for _ in player_keys]


# --- Set all bots to use same logic for now ---
bot_map = {
    "DL": random_bot,
    "RC": random_bot,
    "MU": random_bot,
    "LH": random_bot,
    "SK": random_bot,
    "JP": random_bot,
    "JC": random_bot,
    "CS": random_bot
}
for _ in range(80):
    deck = [(face, rank) for rank in ranks for face in faces]
    random.shuffle(deck)
    betList = [0] * len(players)
    hands = {key: [] for key in player_keys}
    Community = []
    pot = 0
    ante = 1
    bet = 0
    
    # --- Deal hands ---
    for key in player_keys:
        hands[key] = [deck.pop(0), deck.pop(0)]

    # --- Ante Round ---
    while not (all(p[1] == ante or p[0] in [-3,-4] for p in playerStatus) and sum(betList) > 0):
        for i, key in enumerate(player_keys):
            if all(p[1] == ante or p[0] in [-3,-4] for p in playerStatus) and sum(betList) > 0:
                break
            bot_instance = bot_map[key]
            playerStatus[i] = bot_instance.turn(1, ante, betList, i, hands[key], Community,players.values(), playerStatus[i][2], pot)
            ante = max(ante, playerStatus[i][1])
            players[key] = playerStatus[i][2]
            pot = max(pot, playerStatus[i][3])

            betList[i] = ante

    print("ANTE OVER")
    print(f"Ante: {ante}")
    print(f"Final chip counts: {players}")

    
    # --- Deal flop ---
    Community = [deck.pop(0), deck.pop(0), deck.pop(0)]

    # --- Two Betting Rounds ---
    for _ in range(2):
        bet = 0
        for i in range(len(betList)):
            if playerStatus[i][0] in [-1, -2]:  # Fold or Called
                playerStatus[i][0] = 0
                betList[i] = 0
            playerStatus[i][1] = 0

        # Betting round
        while not all_active_players_matched_bet(playerStatus, bet):
            for i, key in enumerate(player_keys):
                if all_active_players_matched_bet(playerStatus, bet):
                    break

                if playerStatus[i][0] in [-3, -4]:  # Folded or All-in
                    playerStatus[i][1] = bet  # Consider them matched
                    continue

                bot_instance = bot_map[key]
                playerStatus[i] = bot_instance.turn(2, bet, betList, i, hands[key], Community,players.values(), playerStatus[i][2], pot)

                bet = max(bet, playerStatus[i][1])
                players[key] = playerStatus[i][2]
                pot = max(pot, playerStatus[i][3])

                if playerStatus[i][0] not in [-3, -4]:
                    betList[i] = playerStatus[i][1]

                if playerStatus[i][0] == -3:
                    print(f"{key} folded.")

        Community.append(deck.pop(0))

    # --- Evaluate Scores ---
    final_scores = []
    for i, key in enumerate(player_keys):
        if playerStatus[i][0] == -3:  # Folded
            final_scores.append((key, -1))  # Disqualified score
        else:
            final_scores.append((key, pm.evaluateHand(hands[key] + Community)))

    print("Final Scores:", final_scores)

    # --- Build Contribution List ---
    contributions = {key: 2000 - playerStatus[i][2] for i, key in enumerate(player_keys)}

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

    # --- Sort scores descending ---
    final_scores.sort(key=lambda x: x[1], reverse=True)

    # --- Distribute Side Pots ---
    for eligible, side_amount in side_pots:
        # From the best score down, find eligible winner(s)
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
            for winner in side_winners:
                players[winner] += share

    print(f"Final chip counts: {players}")

    for i, key in enumerate(player_keys):
        if playerStatus[i][2] <= 0:
            playerStatus.pop(i)
            player_keys.pop(i)
            players.pop(key)
    if len(player_keys) == 1:
        print(f"Final Winner is {players}")
        break
        
    players = list(players.items())

    res = [test_dict[(i - 1) % len(test_dict)]
       for i, x in enumerate(test_dict)]

    res = {sub[0]: sub[1] for sub in res}
    players=res
    player_keys= player_keys[-1:]+player_keys[:-1]
    playerStatus = playerStats[-1:]+playerStatus[:-1]

