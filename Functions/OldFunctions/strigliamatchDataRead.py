#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 12:13:51 2020

Function used to read the results database and process its data. This data is
then linked to the specific players.

@author: SLM
"""

import sys
import os
from pathlib import Path
sys.path.append(os.getcwd())
import strigliamatchLib as sm
import pandas as pd
# TODO: gestione agnostica delle path.
folderPath = Path("../DATA/");

# Creation of the data folder path if not already existing.
if not(os.path.isdir(folderPath)):
       os.mkdir(folderPath);

# Database file path creation.
databaseFile = str(folderPath / "database") + ".pbz2";

if os.path.exists(databaseFile):
    database = sm.decompressPickle(databaseFile)
else:
    database = {}
    
# Data input method selection.
mode = input('Please select input method (file or prompt): ').lower();
while (mode != ('file') and mode != ('prompt')):
    print('\nThe chosen method is not available. Please write \'file\' or \'prompt\'');
    mode = input('\nPlease select input method (file or prompt): ').lower();

# TODO: decommentare i metodi di inserimento.
if mode == 'prompt':
    print('\nLoading new data from prompt...');
    sm.dataInputPrompt(database, databaseFile);
elif mode == 'file':
    print('\nLoading new data from file...');
    try:
        date = pd.to_datetime(input('\nInsert date from which import the new data: '));
    except:
        print('\nInserted date is not valid, please retry.')
        raise Exception('exit');                       
    # newData = sm.dataInputFile();
else:
    print('\nWARNING: an error in data input has occured. Please retry.');
    raise Exception('exit');