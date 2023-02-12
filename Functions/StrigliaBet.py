# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 17:19:00 2020

Script used to analyze the win percentage of 2 teams.

@author: Avvocato
"""

import sys
import os
# sys.path.append(os.getcwd())

from strigliamatchLib import decompressPickle
from pathlib import Path

folderPath = Path("..//DATA//");
databaseFile = str(folderPath / "database") + ".pbz2";

if os.path.exists((folderPath / 'Database.pbz2')):
    database = decompressPickle(databaseFile)
else:
    print('Non ci sono dati nel database.')
    sys.exit()


noOfWhitePlayers = int(input('Inserire numero giocatori squadra BIANCA: '))
# Inserimento squadra colorata, risultato estrapolato da risultato squadra bianca."
noOfColoredPlayers = int(input('Inserire numero giocatori squadra COLORATA: '));
minMatches = int(input('Inserire numero minimo di partite per rientrare in statistica: '))
whiteTeam = [];
coloredTeam = [];

for idx in range(noOfWhitePlayers):
    playerName = input('Inserire nome giocatore ' + str(idx+1) + ': ')
    whiteTeam.append(playerName);
    
for idx in range(noOfColoredPlayers):
    playerName = input('Inserire nome giocatore ' + str(idx + 1) + ': ')
    coloredTeam.append(playerName);
    
whiteMean = 0;
whitePlayers = 0;
for idx in range(len(whiteTeam)):
    if whiteTeam[idx] in database:
        if database[whiteTeam[idx]].noOfMatches >= minMatches:
            whiteMean += (database[whiteTeam[idx]].noOfVictories/
                          database[whiteTeam[idx]].noOfMatches)
            whitePlayers += 1
whiteMean = whiteMean/whitePlayers

coloredMean = 0;
coloredPlayers = 0;
for idx in range(len(coloredTeam)):
    if coloredTeam[idx] in database:
        if database[coloredTeam[idx]].noOfMatches >= minMatches:
            coloredMean += (database[coloredTeam[idx]].noOfVictories/
                          database[coloredTeam[idx]].noOfMatches)
            coloredPlayers += 1
coloredMean = coloredMean/coloredPlayers
        
if whitePlayers < 3 or coloredPlayers < 3:
    print('\r\nATTENZIONE! Statistiche non significative, almeno una delle due squadre ha dati per meno di 3 giocatori.')
print('\r\nLa percentuale di vittoria della squadra bianca è del %.2f%%' % (whiteMean*100));
print('La percentuale di vittoria della squadra colorata è del %.2f%%' % (coloredMean*100));

# A proportion between the 2 win percentages is done and the probability of
# victory is calculated.
# whiteMean : (whiteMean + coloredMean) = victoryProb : 100

whiteVictoryProb = (whiteMean*100)/(whiteMean + coloredMean);
print('\r\nLa probabilità di vittoria della squadra bianca è del %.2f%%' % (whiteVictoryProb));
print('La probabilità di vittoria della squadra colorata è del %.2f%%' % (100 - whiteVictoryProb));