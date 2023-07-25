import matplotlib.pyplot as plt
import random
import math

# Note that several variables are lists solely for matplotlib
num_simulations = 100
max_num_comparisons = 1000
player_bet = 0.96925 # Theoretical neutral player bet
house_bet = 49.03075 # Theoretical neutral house bet
load = num_simulations / 20 # Possibly redundant
win_probability = []
end_balance = []
win_probabilities = []
end_balances = []
win_probabilities_std = []
end_balances_std = []
win_probabilities_ci = []
end_balances_ci = []
num_simulations_list = list(range(1, num_simulations + 1))
end_bal_accept_sim_marker = 5
win_prob_accept_sim_marker = 5
end_balance_threshold = 50
win_probability_threshold = 0.001

# Print load progress in terminal
def update_load(progress):
    bar_length = 30
    filled_length = int(bar_length * progress)
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    percentage = int(progress * 100)
    print(f'\r[{bar}] {percentage}% ', end='', flush=True)

# Driver for card compare game
def card_compare():
    deck = list(range(1, 53)) # Standard 52 card deck
    random.shuffle(deck)
    player_card = random.choice(deck)
    house_card = deck.pop()
    return player_card == house_card

# Create a figure object
fig = plt.figure()
plt.title("Card Compare (" + str(num_simulations) + " Simulations)")
plt.xlabel("Comparison Number")
plt.ylabel("Balance ($)")
plt.xlim([0, max_num_comparisons])

# Loops through each simulation
for simulation in range(num_simulations):
    balance = [0]
    num_comparisons = [0]
    num_wins = 0
    while num_comparisons[-1] < max_num_comparisons:
        same = card_compare()
        if same:
            balance.append(balance[-1] + house_bet)
            num_wins += 1
        else:
            balance.append(balance[-1] - player_bet)
        num_comparisons.append(num_comparisons[-1] + 1)

    win_probability.append(num_wins / num_comparisons[-1])
    end_balance.append(balance[-1])

    overall_win_probability = sum(win_probability) / len(win_probability)
    overall_end_balance = sum(end_balance) / len(end_balance)

    # The statistics library can do this more simply, but requires n >= 2. Since n can be <2 here, we can calculate it manually
    # Note that the first two standard deviations on graph 2 and 3 are incorrect, but for the sake of the analysis, this can be overlooked 
    win_probability_std = math.sqrt(sum((x - overall_win_probability) ** 2 for x in win_probability) / (simulation + 1))
    end_balance_std = math.sqrt(sum((x - overall_end_balance) ** 2 for x in end_balance) / (simulation + 1))

    z_value = 1.96 # z value for 95% confidence interval, consult a z table for other confidence intervals
    win_probability_ci = z_value * win_probability_std / math.sqrt(simulation + 1)
    end_balance_ci = z_value * end_balance_std / math.sqrt(simulation + 1)

    win_probabilities.append(overall_win_probability)
    end_balances.append(overall_end_balance)
    win_probabilities_std.append(win_probability_std)
    end_balances_std.append(end_balance_std)
    win_probabilities_ci.append(win_probability_ci)
    end_balances_ci.append(end_balance_ci)

    plt.plot(num_comparisons, balance)
    progress = simulation / num_simulations
    update_load(progress)

update_load(1) # Call load method one more time so that the loading bar can complete at 100% instead of 99%

# Create figure objects for end balance and win probability
legend_bal_avg = "avg_bal_change = $" + str(round(overall_end_balance, 2))
legend_win_prob = "avg_win_prob = " + str(round(overall_win_probability * 100, 2)) + "%"
plt.plot([], marker="o", label=legend_bal_avg)
plt.plot([], marker="o", label=legend_win_prob)
plt.legend(loc="lower left")
plt.show()

# Seperate simulations above and below threshold, and restrict confidence interval domain
end_balance_under_threshold = 0
win_probability_under_threshold = 0

valid_end_bal_sims = []
valid_win_prob_sims = []
for i in range(1, len(num_simulations_list)):
    if end_balances_ci[i - 1] <= end_balance_threshold:
        end_balance_under_threshold += 1
        valid_end_bal_sims.append([end_balances_ci[i - 1], num_simulations_list[i]])

    if win_probabilities_ci[i - 1] <= win_probability_threshold:
        win_probability_under_threshold += 1
        valid_win_prob_sims.append([win_probabilities_ci[i - 1], num_simulations_list[i]])

error_buffer = 10 # arbitrary buffer of 10 (to address red point bug)
new_valid_end_bal_sims = []
for i in range(len(valid_end_bal_sims)):
    if i >= error_buffer:
        new_valid_end_bal_sims.append(valid_end_bal_sims[i])

new_valid_win_prob_sims = []
for i in range(len(valid_win_prob_sims)):
    if i >= error_buffer:
        new_valid_win_prob_sims.append(valid_win_prob_sims[i])

plt.figure(figsize=(10, 6))
plt.errorbar(num_simulations_list, end_balances, yerr=end_balances_ci, fmt='o-', label='Average Balance')

# Add confidence intervals for the mean
mean_end_balances = []
for i in range(len(end_balances)):
    sum_end_bal = 0
    for j in range(i + 1):
        sum_end_bal += end_balances[j]
    mean = sum_end_bal / (i + 1)
    mean_end_balances.append(mean)

lower_bound = []
upper_bound = []
for i in range(len(mean_end_balances)):
    mean = mean_end_balances[i]
    ci = end_balances_ci[i]
    lower_bound.append(mean - ci)
    upper_bound.append(mean + ci)

plt.fill_between(num_simulations_list, lower_bound, upper_bound, alpha=0.3)

# Express convergence condition as coloured points
x_end_balance = []
y_end_balance = []
for point in new_valid_end_bal_sims:
    x_end_balance.append(point[1])
    y_end_balance.append(point[0])

color = 'red'
for i, (x, y) in enumerate(zip(x_end_balance, y_end_balance)):
    if i >= 5:
        color = 'lime'
    plt.scatter(x, y, color=color)

if len(new_valid_end_bal_sims) >= end_bal_accept_sim_marker:
    x_accept_marker_end_balance = new_valid_end_bal_sims[end_bal_accept_sim_marker][1]
    y_accept_marker_end_balance = new_valid_end_bal_sims[end_bal_accept_sim_marker][0]
    plt.scatter(x_accept_marker_end_balance, y_accept_marker_end_balance, color='orange',
                label='Convergence Threshold for End Balance')

plt.xlabel('Number of Simulations')
plt.ylabel('End Balance ($)')
plt.title("Average End Balance (" + str(num_simulations) + " Simulations)")
plt.grid(True)
plt.show()

plt.figure(figsize=(10, 6))
plt.errorbar(num_simulations_list, win_probabilities, yerr=win_probabilities_ci, fmt='o-', label='Win Probability')

# Add confidence intervals for the mean
mean_win_probabilities = []
for i in range(len(win_probabilities)):
    sum_win_prob = 0
    for j in range(i + 1):
        sum_win_prob += win_probabilities[j]
    mean = sum_win_prob / (i + 1)
    mean_win_probabilities.append(mean)

lower_bound = []
upper_bound = []
for i in range(len(mean_win_probabilities)):
    mean = mean_win_probabilities[i]
    ci = win_probabilities_ci[i]
    lower_bound.append(mean - ci)
    upper_bound.append(mean + ci)

plt.fill_between(num_simulations_list, lower_bound, upper_bound, alpha=0.3)

# Express convergence condition as coloured points
x_win_prob = []
y_win_prob = []
for point in new_valid_win_prob_sims:
    x_win_prob.append(point[1])
    y_win_prob.append(point[0])

color = 'red'
for i, (x, y) in enumerate(zip(x_win_prob, y_win_prob)):
    if i >= 5:
        color = 'lime'
    plt.scatter(x, y, color=color)

if len(new_valid_win_prob_sims) >= win_prob_accept_sim_marker:
    x_accept_marker_win_prob = new_valid_win_prob_sims[win_prob_accept_sim_marker][1]
    y_accept_marker_win_prob = new_valid_win_prob_sims[win_prob_accept_sim_marker][0]
    plt.scatter(x_accept_marker_win_prob, y_accept_marker_win_prob, color='orange',
                label='Convergence Threshold for Win Probability')

plt.xlabel('Number of Simulations')
plt.ylabel('Win Probability')
plt.title("Average Win Probability (" + str(num_simulations) + " Simulations)")
plt.grid(True)
plt.show()
