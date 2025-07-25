# Card-Compare
### Introduction
This project simulates a card comparison game that you've likely encountered at some point in your life, where a player and a house draw cards from a standard 52 card deck. If the cards match then the player wins, and if they don't, the house wins. Through various statistical approaches, this algorithm computes and visualizes the outcomes of this simple card game over several simulations. This Monte Carlo analysis models how experimental values converge to theoretical values, how error gradually dissipates as confidence in an emerging data trend increases, and how to maximize the long-term suffering of your opponent. Okay, maybe not that last one.

(Note that Monte Carlo simulations like these are often used as a heuristic approach to problems that are deterministic yet complex. This card game is not very complex, which makes it much easier to analyze.)

### Graph 1 (100 Simulations)
The probability of a player choosing a card that matches the last card in the deck that the house flips over is 1/52, or roughly 1.92308%. We can easily determine the probability of the house winning by using the complement rule, which involves subtracting the probability of the house winning from the whole, 1 - 1/52, which is roughly 98.07692%. We can expect that over a large number of games, the win/loss percentages should roughly match these probabilities - exactly the outcome we would expect by following the law of large numbers. Instead of taking my word for it, we can run this code with the same inputs that we used for the theoretical calculation and examine the results for ourselves.

In the interest of making this problem a little easier to understand, I've divided both of these numbers by 2. I've also expressed each amount in terms of money, so instead of imagining players betting with percentages, we can imagine betting with real money. This is all to say: when a large number of games are played, the player bets $0.96925, and the house bets $49.03075, we can expect the total winnings to neither fall in favour of the house or the player.

<p align='center'>
  <img src="https://github.com/GoldPapaya/Card-Compare/assets/93890310/38b44aba-8316-4adc-83ef-4512b5b8b7cf" width="600"/>
</p>

After processing 100 simulations with 1,000 games in each simulation (100,000 games total), the above graph holds that the average balance change is -$8.25 which is remarkably close to no change at all. Even with 100,000 games all being played independantly, each with their own end balances, the true average across all of these games tends towards the theoretical expected value. This represents the underlying idea behind the Central Limit Theorem, which states that with a large collection of independent random samples, a normal distribution about a mean (in this case, a mean of 0) is expected.

An astute statistician may notice that this project would benefit from incorporating a confidence interval, so that a quantitative can be used to judge these metrics instead of a loose observation. There is certainly room for further analysis in this program that has been left aside for future projects.

### Graph 2 (Average End Balance) and Graph 3 (Average Win Probability)
<p align='center'>
  <img src="https://github.com/GoldPapaya/Card-Compare/assets/93890310/fbfa7aff-3480-4342-9c82-8dca46036553" width="400"/>
  <img src="https://github.com/GoldPapaya/Card-Compare/assets/93890310/71bfe664-c9a5-4eba-a495-d13b6cad3e44" width="400"/>
</p>

As the number of simulations increases, the convergence of the end balance towards $0 and the win probability towards 1.92% is clear in the graphs above. Prehaps the most powerful element of this code is that it can be applied to any range of pre-determined conditions - you could model the behaviour of this Monte Carlo game as you vary the reward structure for the player/house, as an example. Simulations like these function as a powerful brute-force method to bypass the often complex mathematics often involved with bloated statistics work. When the complexity of a system is extremely high, it's often way more practical to turn to empirical observation than to deal with theory, which is often incomplete or just difficult to interpret.

This code can be used to run simulations for any game or computation, as it is Turing-complete by nature. The graphs simply exist to visualize the results of the game. You could also adjust the amount of simulations, as this will influence the amount of certainty of the end result (more simulations = higher certainty, but also higher compute).

#### Note
Program runtime can still be dramatically improved by leveraging NumPy functions in more places, as array processing in C with many samples is much faster than in Python.
