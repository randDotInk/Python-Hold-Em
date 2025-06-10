import PokerMoves as pm
import random
import bot

faces = ["S", "H", "D", "C"]
ranks = ['2', '3', '4', '5', '6','7', '8', '9', '10', "J", "Q", "K",'A']
deck = list((face, rank) for rank in ranks for face in faces)
random.shuffle(deck)

players = dict(DL=2000, RC=2000, MU=2000, LH=2000, SK=2000, JP=2000, JC=2000, CS=2000)
player_keys = list(players.keys())
playerStatus = [[0, 0, 2000, 0] for _ in player_keys]
playersIn = list(players.keys())
betList = [0] * len(players)
hands = {key: [] for key in player_keys}
Community = []
pot = 0
ante = 1
bet = 0

# --- Ante Round ---
while not (all(p[1] == ante for p in playerStatus) and sum(betList) > 0):
    for i, key in enumerate(player_keys):
        if all(p[1] == ante for p in playerStatus) and sum(betList) > 0:
            break
        playerStatus[i] = bot.turn(1, ante, betList, i, hands[key], Community, playerStatus[i][2], pot)
        if ante <= playerStatus[i][1]:
            ante = playerStatus[i][1]
        players[key] = playerStatus[i][2]
        if pot <= playerStatus[i][3]:
            pot = playerStatus[i][3]
        betList[i] = ante
print("ANTE OVER")

# --- Deal Hands ---
for key in player_keys:
    hands[key] = [deck.pop(0), deck.pop(0)]

# --- Deal First 3 Community Cards ---
Community = [deck.pop(0), deck.pop(0), deck.pop(0)]

# --- Two Betting Rounds ---
for _ in range(2):
    bet = 0
    for i in range(len(betList)):
        if playerStatus[i][0] in [-1, -2]:  # Fold or Called
            playerStatus[i][0] = 0
            betList[i] = 0
        playerStatus[i][1] = 0

    while not (all(q[1] == bet for q in playerStatus) and sum(betList) > 0):
        for i, key in enumerate(player_keys):
            if all(q[1] == bet for q in playerStatus) and sum(betList) > 0:
                break
            if playerStatus[i][0] in [-3, -4]:  # Fold or All-In
                playerStatus[i][1] = bet
                continue
            playerStatus[i] = bot.turn(2, bet, betList, i, hands[key], Community, playerStatus[i][2], pot)
            if bet <= playerStatus[i][1]:
                bet = playerStatus[i][1]
            players[key] = playerStatus[i][2]
            if pot <= playerStatus[i][3]:
                pot = playerStatus[i][3]
            betList[i] = bet

    Community.append(deck.pop(0))

# --- Determine Winner ---
final_scores = []
for i, key in enumerate(player_keys):
    if playerStatus[i][0] in [-3]:  # Folded
        final_scores.append((key, 0.0))
    else:
        score = pm.evaluateHand(hands[key] + Community)
        final_scores.append((key, score))

# Find highest score
final_scores.sort(key=lambda x: x[1], reverse=True)
winner_score = final_scores[0][1]
winners = [name for name, score in final_scores if score == winner_score]

# Split pot
winner = winners[0]
players[winner] += pot

print("\n--- GAME RESULT ---")
print(f"Community Cards: {Community}")
for key in player_keys:
    print(f"{key}: {hands[key]}")
print(f"Winners: {winners} with score {winner_score}")
print(f"Winner receives {winner}")
print(f"Final chip counts: {players}")



