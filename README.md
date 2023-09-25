# Card-Compare
(I still need to finish writing this readme)
### Introduction
This project simulates a simple card comparison game that you've likely encountered at some point in your life. In this game, two players (player and house) draw cards from a standard 52 card deck. If the cards match, the player wins; otherwise, the house wins. Through various statistical approaches, this algorithm computes and then visualizes parameters that are scaled over a very large number of simulations. This monte carlo analysis models how experimental values converge to theoretical values, how error dissipates as confidence in emerging data trends increases, and how to maximize the long-term suffering of your opponent. Okay, maybe not that last one.

### Graph 1
The probability of a player choosing a card that matches the last card in the deck that the house flips over is 1/52, or roughly 1.92308%. We can easily determine the probability of the house winning by taking subtracting the probability of the house winning from the whole, or 1 - 1/52, which is roughly 98.07692%. We can expect that over a large number of games, the win/loss percentages should roughly match these thresholds. Instead of taking my word for it, we can run this code with the same inputs that we used for the theoretical calculation and examine the results for ourselves.

In the interest of making this problem a little easier to understand, I've divided both of these numbers by 2. I've also expressed each amount in terms of money, so instead of imagining players betting with percentages, we can imagine betting with real money. This is all to say: when a large number of games are played, the player bets $0.96925, and the house bets 49.03075, we can expect the total winnings to neither fall in favour of house or player.

![Figure_1](https://github.com/GoldPapaya/Card-Compare/assets/93890310/38b44aba-8316-4adc-83ef-4512b5b8b7cf)
![Figure_2](https://github.com/GoldPapaya/Card-Compare/assets/93890310/fbfa7aff-3480-4342-9c82-8dca46036553)
![Figure_3](https://github.com/GoldPapaya/Card-Compare/assets/93890310/71bfe664-c9a5-4eba-a495-d13b6cad3e44)
