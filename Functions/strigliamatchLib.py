# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 16:39:50 2020

This library contains all the major functions used for database management
and data plotting.

@author: SLM
"""

import bz2
import _pickle as cPickle
import pandas as pd
import datetime
from pathlib import Path
import sys
import os

sys.path.append(os.getcwd())

def compressPickle(title, data):
    """ Function used to compress the database.
    Arguments:
        * title -> file name and directory.
        * data -> data to save in the file. """
    if not(title[-4:] == '.pbz2'):
        title = title + '.pbz2';
    with bz2.BZ2File(str(title), 'wb') as f: 
        cPickle.dump(data, f)

def decompressPickle(filename):
    """ Function used to recover compressed data.
    Arguments:
        * filename -> file directory and name."""
    if not(filename[-5:] == '.pbz2'):
        filename = filename + '.pbz2';
    data = bz2.BZ2File(str(filename), 'rb');
    data = cPickle.load(data);
    return data

class Player:
    """ Class that contains all the parameters and methods used to create a
    player and save its data. """
    def __init__(self, name, noOfMatches = 0, noOfVictories = 0,
                 noOfLosses = 0, whiteMatches = 0, coloredMatches = 0,
                 noOfGoals = 0
                 ):
        """ All of starting parameters are initialized here."""
        self.name = name
        self.noOfMatches = noOfMatches
        self.noOfVictories = noOfVictories
        self.noOfLosses = noOfLosses
        self.whiteMatches = whiteMatches
        self.coloredMatches = coloredMatches
        self.noOfGoals = 0;
        
    def addWhiteMatch(self, result):
        """ Method used to add a white match and its results.
        Arguments:
            * result -> if 1, a white match with a victory is added. If 0, a
            white match with loss is added. """
        self.noOfMatches = self.noOfMatches + 1;
        self.whiteMatches = self.whiteMatches + 1;
        if result:
            self.noOfVictories = self.noOfVictories + 1;
        else:
            self.noOfLosses = self.noOfLosses + 1;
            
    def addColoredMatch(self, result):
        """ Method used to add a colored match and its results.
        Arguments:
            * result -> if 1, a colored match with a victory is added. If 0, a
            colored match with loss is added. """
        self.noOfMatches = self.noOfMatches + 1;
        self.coloredMatches = self.coloredMatches + 1;
        if result:
            self.noOfVictories = self.noOfVictories + 1;
        else:
            self.noOfLosses = self.noOfLosses + 1;
            
    def addCompanion(self, companion, result):
        """ Adds a match with a specific companion and its result.
        Arguments:
            * companion -> name of the companion.
            * result -> match result. """
        if not("companions" in self.__dict__):
            self.companions = {};
            self.companionWins = {};
        if companion in self.companions:
            self.companions[companion] += 1;
            if result:
                self.companionWins[companion] += result;
        else:
            self.companions[companion] = 1;
            self.companionWins[companion] = result;
            
    def addRival(self, rival, result):
        """ Adds a match against a specific rival and its result.
        Arguments:
            * rival -> name of the rival.
            * result -> match result. """
        if not("rivals" in self.__dict__):
            self.rivals = {};
            self.rivalWins = {};
        if rival in self.rivals:
            self.rivals[rival] += 1;
            if result:
                self.rivalWins[rival] += result;
        else:
            self.rivals[rival] = 1;
            self.rivalWins[rival] = result;
            
    def addGoals(self, goals):
        """ FOR FUTUREPROOFING.
        Method that adds the number of goals.
        Arguments:
            * goals -> number of goals."""
        self.noOfGoals += goals;
        
    def presentYourself(self):
        """ FOR TESTING.
        A simple method that gives some basical information on a player."""
        print("Salve, sono " + self.name + ".");
        print("Ho giocato " + str(self.noOfMatches) +" partite.")
        if self.whiteMatches > self.coloredMatches :
            print("Gioco molto spesso con la maglia bianca.")
        else:
            print("Gioco molto spesso con la maglia colorata.")
        if self.noOfVictories > self.noOfLosses:
            print("Vinco molto spesso.")
        else:
            print("A volte vinco.")
        companionsOrdered = {};
        companionsOrdered = {key:value for key, value in
                                 sorted(self.companions.items(),
                                        key=lambda item: item[1],
                                        reverse = True)}
        companionsOrdered = list(companionsOrdered)
        print("Il compagno con cui gioco più spesso è " +
              companionsOrdered[0])
            
def dataInputFile(filename, date, **kwargs):
    """ Function used to load the new data from a file and store it in the
    database.
    Arguments:
        * filename -> file name (default directory: ..\DATA\).
        * date -> date from which take the new data.
    Optional arguments:
        * filepath -> file directory when it's not the default one.
    """
    if filename[-4:] != ".csv":
        filename = filename + ".csv";
    df = pd.read_csv(filename, sep=',');
    df.loc[:, 'Data'] = pd.to_datetime(df.loc[:, 'Data']);
    newData = pd.DataFrame(columns=list(df));
    for idx in range(1,int(df.count()[0])):
        if df.iloc[idx][0] >= date:
            newData = newData.append(df.loc[idx], ignore_index = True);
    
    return newData

def dataInputPrompt(**kwargs):
    """ Function used to load manually new data from prompt and store it in
    the database.
    """
        
    # TODO: eventuale aggiunta di path database personalizzate con argomenti
    # facoltativi della funzione.
    
    # TODO: gestione agnostica delle path.
    folderPath = Path("../DATA/");
    
    # Creation of the data folder path if not already existing.
    if not(os.path.isdir(folderPath)):
           os.mkdir(folderPath);
    
    # Database file path creation.
    databaseFile = str(folderPath / "database") + ".pbz2";
    
    if os.path.exists(databaseFile):
        database = decompressPickle(databaseFile)
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
        playerName = input('Inserire nome giocatore ' + str(idx+1) +
                           ' squadra bianca: ')
        whiteTeam.append(playerName);
        if playerName in database:
            database[playerName].addWhiteMatch(whiteResult);
        else:
            database[playerName] = Player(playerName);
            database[playerName].addWhiteMatch(whiteResult);
        
    
    for idx in range(noOfColoredPlayers):
        playerName = input('Inserire nome giocatore ' + str(idx + 1) + 
                           ' squadra colorata: ')
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
            
    
    
    compressPickle(str(folderPath / "database"), database)
        
    dateBU = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    compressPickle(str(folderPath / ("database_" + dateBU)), database)
    
def dataInputFile(filePath, startingDate, **kwargs):
    """Function used to import results directly from an .ods or .xls file.
    
    Arguments:
        - filePath: complete path (with extension) from which copy the results.
        - startingDate: date from which start adding data (format: yy-mm-dd).
        
    Additional arguments:
        - newDb: if true, doesn't load the old database and creates a new one
        instead.
    """
    # TODO: implementare un metodo furbo per non ricaricare sempre tutti i
    # risultati, ma aggiungere solo quelli nuovi.
    if "newDb" in kwargs.keys():
        newDb = kwargs["newDb"];
    else:
        newDb = False;
    
    folderPath = Path("../DATA/");

    # Creation of the data folder path if not already existing.
    if not(os.path.isdir(folderPath)):
           os.mkdir(folderPath);
    
    # Database file path creation.
    databaseFile = str(folderPath / "database") + ".pbz2";
    
    if os.path.exists(databaseFile) and newDb == False:
        database = decompressPickle(databaseFile)
    else:
        database = {}
    
    startingDate = pd.to_datetime(startingDate);
    df = pd.read_excel(filePath);
    
    df["Data"] = pd.to_datetime(df["Data"]);
    
    # dateTemp = pd.to_datetime(startingDate);
    idxDate = 0;
    
    # Si arriva al primo indice con la data giusta.
    while (df["Data"][idxDate] < startingDate):
        idxDate += 1;
    # tempDate = startingDate;
    tempIdx = idxDate;
    
    # TODO: testare cosa succede con starting date diverse.
    while (idxDate < df["Data"].count()):
        whiteResult = [];
        coloredResult = [];
        whiteTeam = [];
        coloredTeam = [];
        while tempIdx < df["Data"].count() and df["Data"][tempIdx] == df["Data"][idxDate]:
            # Vengono create le squadre e salvato il risultato.
            if df["Squadra"][tempIdx] == "B":
                whiteTeam.append(df["Giocatore"][tempIdx]);
                whiteResult = df["Risultato"][tempIdx];
                tempIdx += 1;
            else:
                coloredTeam.append(df["Giocatore"][tempIdx]);
                coloredResult = df["Risultato"][tempIdx];
                tempIdx += 1;
        
        # Inserimento risultati partita ed aggiunta giocatori al database in caso
        # non siano ancora presenti.
        idxTeam = 0;
        for idxTeam in range(len(whiteTeam)):
            if whiteTeam[idxTeam] in database:
                database[whiteTeam[idxTeam]].addWhiteMatch(whiteResult);
            else:
                database[whiteTeam[idxTeam]] = Player(whiteTeam[idxTeam]);
                database[whiteTeam[idxTeam]].addWhiteMatch(whiteResult);
        idxTeam = 0;
        for idxTeam in range(len(coloredTeam)):
            if coloredTeam[idxTeam] in database:
                database[coloredTeam[idxTeam]].addColoredMatch(coloredResult);
            else:
                database[coloredTeam[idxTeam]] = Player(coloredTeam[idxTeam]);
                database[coloredTeam[idxTeam]].addColoredMatch(coloredResult);
        
        # Inserimento statistiche su compagni di squadra.
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
        idxDate = tempIdx;       
        
        
    compressPickle(str(folderPath / "database"), database)
        
    dateBU = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    compressPickle(str(folderPath / "Archive" / ("database_" + dateBU)), database)
        
        