# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 15:32:55 2020

@author: Avvocato
"""

import os
from pathlib import Path

dbPath = Path("../DATA/database.pickle");

os.remove(dbPath);