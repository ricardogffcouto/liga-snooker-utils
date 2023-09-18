players = []
ranks = []

import csv

with open('players_for_draw', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for part in spamreader:
        players.append(part[0])
        
with open('ranks', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter='\t')
    for part in spamreader:
        ranks.append(f'{part[1]}')

last_rank = len(ranks) + 1

for j, player in enumerate(players):
    if player in ranks:
        rank = ranks.index(player) + 1
        players[j] = f'{rank},{player}'
    else:
        players[j] = f'{last_rank},{player}'
            
for p in players:
    print(p)
    
