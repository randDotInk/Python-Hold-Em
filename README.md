YOu are such a good boy for going to the read me

Rules:
This will be a Texas Hold' Em variant of Poker but I really don't feel like learning the full rules, so there will be some differneces.

The Ante/ Blinds/ Buy-in, will be an agreed upon amount of money that the bots will either raise, call or fold, until all bots desiring to play call.
Please don't make the bot agressive in this part, set a limit of when to fold or stop raising por favor.

I am too lazy to code the dealer moving place, so order will always be the same until an elimination occurs

I too not smart to have multiple programs running so we are using the power of imports!
To create a bot it must be:
-it's own seperate file
-Use the PokerMoves import
-Have a method called turn(stage, Amount, betList, turn, hand, comCards, bank, pot) with these parameters
 What does Each parameter do? - prolly Joshua Power
 stage: either 1 or 2, 1 being the ante phase and 2 being the game phase. Highly recommened you use the stage to determine your plan of action like in the bot examples.
 amount: I was too lazy to write buy-in, but essentially it is the amount to call with.
 betList: This is what the previous players have betted
 turn: This which index you are in the betList
 hand: This the hole cards/ cards in your hand
 comCards: Community Cards
 bank: money you have
 pot: money in pot

DO NOT UPDATE ANY OF THE PARAMETERS IN METHOD

 Now its the moves
 You must return One of the following methods, raiseTo, raiseBy, check, fold, allIn
 raiseTo(bet, Amount, betList, turn, bank, pot): Your bet is the new buy-in you must calculate bet.
 raiseBy(bet, Amount, betList, turn, bank, pot): buy-in is increased by bet so it really just (bet+Amount) you must calculate bet
 check(Amount, betList, turn, bank, pot): Calls the last Raise
 fold(Amount, betList, turn, bank, pot): folds
 allIn(Amount, betList, turn, bank, pot): goes all in

 Please no touchy the parameter of the actions
