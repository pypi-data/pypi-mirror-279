#Shapley-Shubik voting power






# Example usage



if __name__ == '__main__':
    from itertools import permutations
    def calculate_shapley_shubik(players, weights):
        n = len(players)
        total_weight = sum(weights)
        shapley_shubik = {player: 0 for player in players}
        for perm in permutations(players):
            cumulative_weight = 0
            for i, player in enumerate(perm):
                cumulative_weight += weights[players.index(player)]
                if cumulative_weight > total_weight / 2:
                    shapley_shubik[player] += 1
                    break
        for player in players:
            shapley_shubik[player] /= len(list(permutations(players)))
        return shapley_shubik
    players = ['Alice', 'Bob', 'Charlie']
    weights = [3, 2, 5]
    voting_power = calculate_shapley_shubik(players, weights)
    print("Shapley-Shubik Voting Power:")
    for player, power in voting_power.items():
        print(f"{player}: {power:.2f}")
