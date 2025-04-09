
class Player:
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.resistance_points = 0
        self.sonnenborn_berger = 0
        self.black = 0
        self.opponents = []


class player_result:
    def __init__(self, name: str, points: float, resistance_points: float, sonnenborn_berger: float, black: int):
        self.name = name
        self.points = points
        self.resistance_points = resistance_points
        self.sonnenborn_berger = sonnenborn_berger
        self.black = black

    def __str__(self):
        return 'player_result(name=\'' + self.name + '\', points=' + str(self.points) + ', resistance_points=' + \
               str(self.resistance_points) + ', sonnenborn_berger=' + str(self.sonnenborn_berger) + \
               ', black=' + str(self.black) + ')'

    def __eq__(self, other):
        return self.name == other.name and self.points == other.points and \
               self.resistance_points == other.resistance_points and \
               self.sonnenborn_berger == other.sonnenborn_berger and self.black == other.black


def determine_output(input):
    sections = input.split('\n\n')  # split input into sections
    player_names = sections[0].split('\n')  # get player names from the first section
    players = {name: Player(name) for name in player_names if name}  # create players, ignoring empty names

    rounds = [round.split('\n') for round in sections[1:]]  # get rounds from the remaining sections

    for round in rounds:
        for match in round:
            if match:
                # <white player name> <black player name> <points earned by white player> <points earned by black player>
                white, black, white_points, black_points = match.split()
                white_points, black_points = float(white_points), float(black_points)

                # Add points for each player
                players[white].points += white_points
                players[black].points += black_points

                # Get score of player's opponents
                players[white].opponents.append((players[black], white_points))
                players[black].opponents.append((players[white], black_points))
                
                # Increment black counter for the black player
                players[black].black += 1

    for player in players.values():
        player.resistance_points = sum(opponent.points for opponent, _ in player.opponents)
        player.sonnenborn_berger = sum(opponent.points * result for opponent, result in player.opponents)

    ranking = sorted(players.values(), key=lambda p: (-p.points, -p.resistance_points, -p.sonnenborn_berger, -p.black))

    return [player_result(p.name, p.points, p.resistance_points, p.sonnenborn_berger, p.black) for p in ranking]
