# UNO_GAME
An UNO game made with Pygame that allows you to face off against AIs to rack up wins in the leaderboard, or play against your friends across the same device

In my rendition of UNO there are two ways to win, one by clearing out your hand (the original way), and two by forcing your opponent to draw more than 11 cards. Those are the two ways to win and whoever manages to do either of those actions will win (say if there is a 4 player game amongst friends and player 1 manages to target player 3 and force them with a hand over 11 cards [much harder said than done], the game ends and player 1 is the winner).

How to call UNO?
In original UNO when a player as one card left they must yell UNO first in order to not face the punishment of drawing two cards. I chose to add a speed click minigame, once a player has 1 card in their hand there will be a brief prompt asking you to click now, if you fail to meet the split second window, the program will say TOO SLOW! and force you to draw two cards.

Other than that UNO pretty much functions exactly like normal, there are no different cards compared to the familiar game you know and love. But when playing with multiplayer, once your turn ends it will ask for the device to be passed around, this is because this game is designed to be played multiplayer amongst the same device and there will be an input prompt for the other person when the pass is complete to continue with their turn, ensuring fair game and privacy of their own hand.

Now for the AI, you can play with a bot against UNO and each win against the AI contributes to a win on your account that is stored in an SQL database, there is a leaderboard at the very main page of the top 5 players and their wins, congratulating the very first player in special golden text. There is account creation, logins and recovery. But the recovery improvements still need to take place (i.e. two step verification).

That is pretty much all you have to know. I hope you have enjoyed my NEA project and have fun!
Tha
