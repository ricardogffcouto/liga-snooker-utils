#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Variaveis globais e classes
import math, random, string, time, os, csv

TIME_MULTIPLE = 0.1
DEBUGGING_TIME_MULTIPLE = 100

PLAYERS_PER_GROUP = 3
FIRST_DIVISION_GROUPS = 3
PLAYERS_IN_FIRST_DIVISION = PLAYERS_PER_GROUP * FIRST_DIVISION_GROUPS
DIVISIONS = 2
PROMOTED_PLAYERS = 3
SEEDS = PLAYERS_PER_GROUP
PLAYERS_IN_PROMOTION_PLAYOFF = 6

class Participant():
    def __repr__(self):
        return self.name

    def __init__(self, name, ranking, current_division = 2):
        self.name = name
        self.ranking = ranking
        self.current_division = current_division

class Place():
    def __repr__(self):
        return "{}º do Grupo {} - {}ª Div".format(self.place, self.group, self.division)

    def __init__(self, place, division, group):
        self.place = place
        self.division = division
        self.group = group


class Game():
    def __repr__(self):
        return "Jogo {} - {} x {}".format(self.idx, self.players[0], self.players[1])

    def __init__(self, idx, players):
        self.idx = idx
        self.players = players

participants = []

with open('players_for_draw', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for part in spamreader:
        try:
            div = int(part[2])
        except:
            div = 2
        participants.append(Participant(part[1], int(part[0]), div))

# Alocamento de participantes por divisões
participants_in_divisions = [[], []]

# Alocamento na 1ª Divisão
participants.sort(key=lambda object1: object1.ranking)

os.system("clear")
print()
print("\x1b[1;33mLISTA DE PARTICIPANTES")
print()
print("\x1b[1;37mRanking\t Nome")
for p in participants:
    print("\x1b[0;37m{}\t {}".format(p.ranking, p))


time.sleep(TIME_MULTIPLE * 10)

same_ranking = []
for i, p in enumerate(participants):
    if i != 0:
        if p.ranking == participants[i - 1].ranking:
            if len(same_ranking) > 0:
                if same_ranking[-1][0].ranking == p.ranking:
                    same_ranking[-1].append(p)
                else:
                    same_ranking.append([p, participants[i - 1]])
            else:
                same_ranking.append([p, participants[i - 1]])

if len(same_ranking) > 0:
    os.system("clear")
    print()
    print("\x1b[1;33mSORTEIO DE PARTICIPANTES COM O MESMO RANKING")
    print("\x1b[0;37mQuando 2 ou mais participantes têm o mesmo Ranking da Liga,\ne o critério de desempate (melhor break) não os permite desempatar\né efectuado um sorteio para definir o Ranking de cada um.")
    print()
    print("\x1b[1;37mPARTICIPANTES EMPATADOS:")
    print()
    print("\x1b[1;37mRanking\t Nome")
    for sr in same_ranking:
        for p in sr:
            print("\x1b[0;37m{}\t {}".format(p.ranking, p))
        print()

    time.sleep(TIME_MULTIPLE * 10)
    print("\x1b[1;37mSORTEIO:")
    print()
    for sr in same_ranking:
        random.shuffle(sr)
        for i, p in enumerate(sr):
            p.ranking += i
            print("\x1b[0;37m{}\t {}".format(p.ranking, p))
        print()

    time.sleep(TIME_MULTIPLE * 10)


for p in participants:
    if p.current_division == 1:
        participants_in_divisions[0].append(p)
    if len(participants_in_divisions[0]) == PLAYERS_IN_FIRST_DIVISION:
        break

if len(participants_in_divisions[0]) < PLAYERS_IN_FIRST_DIVISION:
    for p in participants:
        if p.current_division != 1:
            participants_in_divisions[0].append(p)
        if len(participants_in_divisions[0]) == PLAYERS_IN_FIRST_DIVISION:
            break

# Alocamento na 2ª Divisão
for p in participants:
    if p not in participants_in_divisions[0]:
        participants_in_divisions[1].append(p)



# Sorteio do Playoff de Campeão da 2ª Divisão

# Colocação de jogadores em potes

seeds_for_promotion_playoff = [[], [], []]

for g in range(int(len(participants_in_divisions[1]) / PLAYERS_PER_GROUP)):
    seeds_for_promotion_playoff[0].append(Place(place=1, division=2, group=string.ascii_uppercase[g]))

for g in range(PLAYERS_IN_PROMOTION_PLAYOFF - int(len(participants_in_divisions[1]) / PLAYERS_PER_GROUP)):
    seeds_for_promotion_playoff[1].append(Place(place=g+1, division=2, group="de melhores 2ºs classificados"))

# Jogadores e byes no playoff de promoção
amount_of_players_in_promotion_playoff = 0

def nearest_number_to_power_of_two(num):
    for x in range(10):
        if pow(2, x) >= num:
            return pow(2, x)

for s in seeds_for_promotion_playoff:
    amount_of_players_in_promotion_playoff += len(s)

amount_of_byes = nearest_number_to_power_of_two(amount_of_players_in_promotion_playoff) - amount_of_players_in_promotion_playoff

for bye in range(amount_of_byes):
    seeds_for_promotion_playoff[2].append(Participant("Bye", 99, 2))

all_players_in_promotion_playoff = []
for s in seeds_for_promotion_playoff:
    all_players_in_promotion_playoff += s


# Criação dos jogos do Playoff de Campeão da 2ª Divisão

promotion_playoff_games = []

amount_of_promotion_playoff_rounds = int(math.log(len(all_players_in_promotion_playoff)) / math.log(2))

def create_game_round(players, initial_game_number, winner=True):
    amount_of_games = int(len(players) / 2)
    game_round = []

    for g in range(amount_of_games):
        player_1 = players.pop(0)
        if isinstance(player_1, Game):
            if winner:
                player_1 = "Vencedor do Jogo {}".format(player_1.idx)
            else:
                player_1 = "Perdedor do Jogo {}".format(player_1.idx)

        player_2 = players.pop()
        if isinstance(player_2, Game):
            if winner:
                player_2 = "Vencedor do Jogo {}".format(player_2.idx)
            else:
                player_2 = "Perdedor do Jogo {}".format(player_2.idx)

        game_players = [player_1, player_2]

        game_round.append(Game(initial_game_number + g + 1, game_players))

    return game_round

def adjust_first_round_games(games):
    for i, g in enumerate(games):
        if isinstance(g.players[1], Place):
            if g.players[0].group == g.players[1].group:
                player_to_swap = games[i].players[1]
                games[i].players[1] = games[i + 1].players[1]
                games[i + 1].players[1] = player_to_swap
                break

    for i in range(int(math.log(len(games)) / math.log(2)) - 2):
        games[-i-1], games[-i-3] = games[-i-3], games[-i-1]
        temp_idx = games[-i-1].idx
        games[-i-1].idx = games[-i-3].idx
        games[-i-3].idx = temp_idx

    return games

# time.sleep(TIME_MULTIPLE * 15)
# os.system("clear")
# print()

# print("\x1b[1;33mPLAYOFF DE CAMPEÃO DA 2ª DIVISÃO\n")

# initial_game_number = 0

# game_round = create_game_round(all_players_in_promotion_playoff, initial_game_number)
# adjust_first_round_games(game_round)

# for g in game_round:
#     print("\x1b[0;37m{}".format(g))
# print()

# time.sleep(TIME_MULTIPLE * 15 * DEBUGGING_TIME_MULTIPLE)
# os.system("clear")
# print()

# # Todos os jogadores no playoff de Campeão

# print("\x1b[1;33mPLAYOFF DE CAMPEÃO\n")

# all_players_in_champion_playoff = []

# for i in range(2):
#     for g in range(int(len(participants_in_divisions[0]) / PLAYERS_PER_GROUP)):
#         all_players_in_champion_playoff.append(Place(place=i + 1, division=1, group=string.ascii_uppercase[g]))

# # Criação dos jogos do Playoff de Subida

# champion_playoff_games = []

# amount_of_champion_playoff_rounds = 3

# initial_game_number = 0
# for r in range(amount_of_champion_playoff_rounds):
#     if r == 0:
#         print("\x1b[1;37mMeias finais")
#         game_round = create_game_round(all_players_in_champion_playoff, initial_game_number)
#     elif r == 1:
#         print("\x1b[1;37mApuramento do 3º Lugar")
#         game_round = create_game_round(champion_playoff_games[r-1].copy(), initial_game_number, False)
#     elif r == 2:
#         print("\x1b[1;37mFinal")
#         game_round = create_game_round(champion_playoff_games[r-2].copy(), initial_game_number)

#     champion_playoff_games.append(game_round)

#     initial_game_number += len(game_round)

#     for g in game_round:
#         print("\x1b[0;37m{}".format(g))
#     print()

# # Jogo de manutenção na 1ª Divisão

# print("\x1b[1;33mJOGO DE MANUTENÇÃO NA 1ª DIVISÃO\n")

# maintenance_match = []
# for g in range(2):
#     maintenance_match.append(Place(place=3, division=1, group=string.ascii_uppercase[g]))
# print("\x1b[0;37m{} x {}".format(maintenance_match[0], maintenance_match[1]))

# groups, promotion_playoff_games, champion_playoff_games

# 1ª divisão Alocamento de participantes por cabeças de série
participants_in_seeds = [[], []]

def alocate_participants_in_seeds(participants, division_order):
    seed_groups = [[] for x in range(SEEDS)]

    players = sorted(participants, key=lambda object1: object1.ranking)

    amount_of_players_per_seed = math.ceil(len(players) / SEEDS)

    for s in seed_groups:
        for x in range(amount_of_players_per_seed):
            try:
                s.append(players.pop(0))
            except:
                s.append(Participant("Bye", 99, division_order))

    return seed_groups

for d in range(2):
    participants_in_seeds[d] = alocate_participants_in_seeds(participants_in_divisions[d], d + 1)

# Sorteio de participantes por grupos
groups = [[], []]

def print_participants_in_seeds(seeds, division_order):
    time.sleep(TIME_MULTIPLE * 2)
    os.system("clear")
    print()
    print("\x1b[1;33m{}ª DIVISÃO".format(division_order))
    print("\x1b[1;33mSorteio da Fase de Grupos")
    for i, s in enumerate(seeds):
        print()
        print("\x1b[1;37mPote {}".format(i + 1))
        for p in s:
            print("\x1b[0;37m{}\t {}".format(p.ranking, p))
        print()

def print_participants_in_groups(groups, division_order):
    print()
    for g, group in enumerate(groups):
        print("\x1b[1;37m{}ª Divisão - Grupo {}".format(division_order, string.ascii_uppercase[g]))
        for part in group:
            print("\x1b[0;37m{}\t {}".format(part.ranking, part))
        print()


def draw_in_groups(seed_groups, division_order):
    amount_of_groups = len(seed_groups[0])
    print_participants_in_seeds(seed_groups, division_order)
    groups = [[] for x in range(amount_of_groups)]
    print_participants_in_groups(groups, division_order)
    time.sleep(TIME_MULTIPLE * 2)

    for group in groups:
        for s in seed_groups:
            player = random.choice(s)
            i = s.index(player)
            s.pop(i)
            group.append(player)
            print_participants_in_seeds(seed_groups, division_order)
            print_participants_in_groups(groups, division_order)


    return groups

# Mostrar os grupos

time.sleep(TIME_MULTIPLE * 15)

groups[0] = draw_in_groups(participants_in_seeds[0], 1)

time.sleep(TIME_MULTIPLE * 2)
os.system("clear")
print()

print("\x1b[1;33m1ª DIVISÃO")
print("\x1b[1;33mFase de Grupos")
print_participants_in_groups(groups[0], 1)

time.sleep(TIME_MULTIPLE * 5)

groups[1] = draw_in_groups(participants_in_seeds[1], 2)

time.sleep(TIME_MULTIPLE * 2)
os.system("clear")
print()

print("\x1b[1;33m2ª DIVISÃO")
print("\x1b[1;33mFase de Grupos")
print_participants_in_groups(groups[1], 2)

time.sleep(TIME_MULTIPLE * 5)
os.system("clear")

# Criar ficheiro com os nomes dos jogadores para colocar no ficheiro da liga
def save_participants_file(groups):
    file = open('draw', 'w+')
    for division in groups:
        for group in division:
            for participant in group:
                print(participant.name, file=file)

save_participants_file(groups)