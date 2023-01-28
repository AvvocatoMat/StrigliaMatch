# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 16:15:02 2020

@author: SLM
"""

import sys
import os
from pathlib import Path
sys.path.append(os.getcwd())
# Questo si traduce con 'dal file Player.py importa la classe Player
from StrigliaMatchMethod import Player
from StrigliaMatchMethod import compressPickle;
from StrigliaMatchMethod import decompressPickle;
import datetime


folderPath = Path("../DATA/");

if not(os.path.isdir(folderPath)):
       os.mkdir(folderPath);

dataBaseFile = folderPath / "database";

if os.path.exists(str(dataBaseFile) + '.pbz2'):
    database = decompressPickle(str(dataBaseFile) + '.pbz2')
else:
    database = {}

# Inserimento squadra bianca e risultato.
noOfWhitePlayers = int(input('Inserire numero giocatori squadra BIANCA: '))
# Inserimento squadra colorata, risultato estrapolato da risultato squadra bianca."
noOfColoredPlayers = int(input('Inserire numero giocatori squadra COLORATA: '));
go = 0
while not(go):
    whiteResult = int(
        input("Inserire risultato squadra BIANCA (1 = vittoria, 0 = sconfitta): "))
    if whiteResult == 0 or whiteResult == 1:
        go = 1
    else:
        print("Valore inserito non valido. Riprovare.")

coloredResult = int(not(whiteResult))
whiteTeam = [];
coloredTeam = [];

for idx in range(noOfWhitePlayers):
    playerName = input('Inserire nome giocatore ' + str(idx+1) + ': ')
    whiteTeam.append(playerName);
    if playerName in database:
        database[playerName].addWhiteMatch(whiteResult);
    else:
        database[playerName] = Player(playerName);
        database[playerName].addWhiteMatch(whiteResult);
    

for idx in range(noOfColoredPlayers):
    playerName = input('Inserire nome giocatore ' + str(idx + 1) + ': ')
    coloredTeam.append(playerName);
    if playerName in database:
        database[playerName].addColoredMatch(coloredResult);
    else:
        database[playerName] = Player(playerName);
        database[playerName].addColoredMatch(coloredResult);
        
for idx in range(len(whiteTeam)):
    for companionIdx in range(len(whiteTeam)):
        playerName = whiteTeam[idx]
        companionName = whiteTeam[companionIdx]
        if idx != companionIdx:
            database[playerName].addCompanion(companionName, whiteResult)
            
for idx in range(len(coloredTeam)):
    for companionIdx in range(len(coloredTeam)):
        playerName = coloredTeam[idx]
        companionName = coloredTeam[companionIdx]
        if idx != companionIdx:
            database[playerName].addCompanion(companionName, coloredResult)
        


compressPickle(dataBaseFile, database)
    
dateBU = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
compressPickle((folderPath / ("database_" + dateBU)), database)