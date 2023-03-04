# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 12:04:31 2023

@author: SirLawyerMat
"""

import sys
import os
import pandas as pd
# sys.path.append(os.getcwd())
from itertools import combinations, permutations

from strigliamatchLib import decompressPickle
from pathlib import Path

debugging = True;

playerNum = 10;
teamSize = 5;

folderPath = Path("..//DATA//");
databaseFile = str(folderPath / "database") + ".pbz2";
rolesFile = str(folderPath / "roles") + ".xls";

if os.path.exists((folderPath / 'Database.pbz2')):
    database = decompressPickle(databaseFile)
else:
    print('Non ci sono dati nel database.')
    sys.exit()
    
try:
    roles = pd.read_excel(rolesFile);
except:
        print('ATTENZIONE! Nessun file con i ruoli presente. Sarà necessario ' + 
              ' inserire i dati manualmente.')

noOfPlayers = playerNum;

if debugging:
    players = ['Rello', 'Ric', 'Faggio', 'Bocio', 'Dami', 'Bendo', 'Lore', 'Gigi',
               'Cap', 'Flammia'];
    minMatches = 3;
else:
    players = [];
    
    minMatches = int(input('Inserire numero minimo di partite per considerare le statistiche: '))
    
    for idx in range(noOfPlayers):
        playerName = input('Inserire nome giocatore ' + str(idx+1) + ': ')
        players.append(playerName);
        
# Check if players have roles and stats. If not, ask user input.
for idx in range(0, playerNum):
    if not players[idx] in str(roles['Name']):
        go = False;
        while not go:
            role = input('Inserire ruolo per ' + players[idx] + ': ').capitalize();
            tier = int(input('Inserire tier per ' + players[idx] + ': '));
            if (role in ['P', 'A', 'D']) and (int(tier) in [1,2,3]):
                go = True;
                roles = roles.append({'Name':players[idx], 'Role':role, 'Tier':tier}, ignore_index = True);
            else:
                print('ERRORE! Ruolo o tier non validi. Reinserire il dato.');

allTeams = combinations(players, teamSize);
allTeams = list(allTeams);

# Per vedere se un elemento di un team è in un altro:
#    len(set(list1).intersection(list2)) > 0

legalTeams = [];

# Legal teams creation: only couples where elements of one team is not in the
# other are considered.
for idx in range(0, len(allTeams)):
    for idxInt in range(idx, len(allTeams)):
        if not len(set(allTeams[idx]).intersection(allTeams[idxInt])) > 0:
            legalTeams.append([allTeams[idx], allTeams[idxInt]]);




# whiteMean = 0;
# whitePlayers = 0;
# for idx in range(len(whiteTeam)):
#     if whiteTeam[idx] in database:
#         if database[whiteTeam[idx]].noOfMatches >= minMatches:
#             whiteMean += (database[whiteTeam[idx]].noOfVictories/
#                           database[whiteTeam[idx]].noOfMatches)
#             whitePlayers += 1
# whiteMean = whiteMean/whitePlayers

# coloredMean = 0;
# coloredPlayers = 0;
# for idx in range(len(coloredTeam)):
#     if coloredTeam[idx] in database:
#         if database[coloredTeam[idx]].noOfMatches >= minMatches:
#             coloredMean += (database[coloredTeam[idx]].noOfVictories/
#                           database[coloredTeam[idx]].noOfMatches)
#             coloredPlayers += 1
# coloredMean = coloredMean/coloredPlayers
        
# if whitePlayers < 3 or coloredPlayers < 3:
#     print('\r\nATTENZIONE! Statistiche non significative, almeno una delle due squadre ha dati per meno di 3 giocatori.')
# print('\r\nLa percentuale di vittoria della squadra bianca è del %.2f%%' % (whiteMean*100));
# print('La percentuale di vittoria della squadra colorata è del %.2f%%' % (coloredMean*100));

# # A proportion between the 2 win percentages is done and the probability of
# # victory is calculated.
# # whiteMean : (whiteMean + coloredMean) = victoryProb : 100

# whiteVictoryProb = (whiteMean*100)/(whiteMean + coloredMean);
# print('\r\nLa probabilità di vittoria della squadra bianca è del %.2f%%' % (whiteVictoryProb));
# print('La probabilità di vittoria della squadra colorata è del %.2f%%' % (100 - whiteVictoryProb));