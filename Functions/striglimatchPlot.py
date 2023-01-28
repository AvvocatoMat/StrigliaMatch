# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 16:05:38 2020

@author: Avvocato
"""

import sys
import os
sys.path.append(os.getcwd())
from strigliamatchLib import decompressPickle
import matplotlib.pyplot as plt
from pathlib import Path

# TODO: gestione agnostica delle path.
figurePath = Path("../Figures/");
if not(os.path.isdir(figurePath)):
       os.mkdir(figurePath);
       

generalPath = Path("../Figures/___COMMON/");
if not(os.path.isdir(generalPath)):
       os.mkdir(generalPath);

dbPath = Path("../DATA/");
databaseFile = str(dbPath / "database") + ".pbz2";

if os.path.exists(databaseFile):
    dataBase = decompressPickle(databaseFile)
else:
    print("Impossibile procedere. Nessun database disponibile.")

minMatch = int(input("Inserire il numero minimo di partite per rientrare in" + 
                     " statistica: "))
titleSize = 25;
labelSize = 15;

for key in dataBase:
    fig, axs = plt.subplots(2,1)
    fig.set_size_inches([10,8])
    width = 0.5;
    axs[0].bar([1,2], [dataBase[key].noOfVictories,
               dataBase[key].noOfLosses], width, label = 'Vittore/Sconfitte')
    axs[0].set_xticklabels(['Vittorie', 'Sconfitte'], fontsize = labelSize)
    axs[0].set_xticks([1, 2])
    axs[0].set_yticks(range(max([dataBase[key].noOfVictories,
                                 dataBase[key].noOfLosses])+1))
    axs[0].grid(True)
    fig.suptitle(key, fontsize = titleSize, y = 0.95)
    axs[1].bar([1,2], [dataBase[key].whiteMatches,
           dataBase[key].coloredMatches], width, label = 'Bianchi/Colorati')
    axs[1].set_xticklabels(['Bianchi', 'Colorati'], fontsize = labelSize)
    axs[1].set_xticks([1, 2])
    axs[1].set_yticks(range(max([dataBase[key].whiteMatches,
                                 dataBase[key].coloredMatches])+1))
    axs[1].grid(True)
    if not(os.path.isdir(figurePath / key)):
        os.mkdir(figurePath / key)
    plt.savefig(figurePath / key / "Stats.jpg")
    
    
    plt.figure(figsize = (10,8));
    plt.grid(True)
    width = 0.5;
    orderedCompanions = {k:v for k, v in sorted(
        dataBase[key].companions.items(), key=lambda item: item[1],
            reverse = True)}
    plt.bar(range(len(orderedCompanions)),
            list(orderedCompanions.values()), width, align='center',
            label = 'Compagni')
    plt.yticks(ticks = range(max(orderedCompanions.values())+1),
               fontsize = labelSize)
    plt.xticks(range(len(orderedCompanions)),
               [*orderedCompanions], fontsize = labelSize,
               rotation = 'vertical');
    
    plt.title(key + ", compagni di squadra.", fontsize = titleSize)
    plt.savefig(figurePath / key / "Companions.jpg")
    
    plt.figure(figsize = (10,8));
    plt.grid(True)
    width = 0.5;
    orderedCompanions = {k:v for k, v in sorted(
        dataBase[key].companionWins.items(), key=lambda item: item[1],
            reverse = True)}
    plt.bar(range(len(orderedCompanions)),
            list(orderedCompanions.values()), width, align='center',
            label = 'VittorieCompagni')
    plt.yticks(ticks = range(max(orderedCompanions.values())+1),
               fontsize = labelSize)
    plt.xticks(range(len(orderedCompanions)),
               [*orderedCompanions], fontsize = labelSize,
               rotation = "vertical");
    plt.title(key + ", vittorie con i compagni.", fontsize = titleSize)
    plt.savefig(figurePath / key / "CompanionWins.jpg")


# Grafico a barre percentuale di vittorie.
retrievedVictories = {}
retrievedMatches = {}
winPercentages = {}
for key in dataBase:
    retrievedVictories[key] = dataBase[key].noOfVictories
    retrievedMatches[key] = dataBase[key].noOfMatches
    winPercentages[key] = retrievedVictories[key]/retrievedMatches[key]

winPercentagesPurged = {}
for key in winPercentages:
    if retrievedMatches[key] >= minMatch:
        winPercentagesPurged[key] = winPercentages[key]
winPercentagesOrdered = {key:value for key, value in
 sorted(winPercentagesPurged.items(), key=lambda item: item[1], reverse = True)}

plt.figure(figsize = (10,8));
plt.grid(True)
width = 0.5;
plotValues = [100*x for x in list(winPercentagesOrdered.values())]
plt.bar(range(len(winPercentagesOrdered)),
        plotValues, width, align='center',
        label = 'PercentualiVittoria')
ytickslist = range(0,110,10)
plt.yticks(ticks = [*ytickslist],
           fontsize = labelSize)
xtickslist = range(len(winPercentagesOrdered))
plt.xticks([*xtickslist], [*winPercentagesOrdered], fontsize = labelSize,
           rotation = "vertical");
plt.title("Percentuali di vittoria", fontsize = titleSize)
plt.savefig(generalPath / "WinPercentage.jpg")      


matchesOrdered = {key:value for key, value in
 sorted(retrievedMatches.items(), key=lambda item: item[1], reverse = True)}

plt.figure(figsize = (10,8));
plt.grid(True)
width = 0.5;
plotValues = list(matchesOrdered.values())
plt.bar(range(len(matchesOrdered)),
        plotValues, width, align='center',
        label = 'PartiteGiocate')
ytickslist = range(max(plotValues)+1)
plt.yticks(ticks = [*ytickslist],
           fontsize = labelSize)
xtickslist = range(len(matchesOrdered))
plt.xticks([*xtickslist], [*matchesOrdered], fontsize = labelSize,
           rotation = "vertical");
plt.title("Partite giocate", fontsize = titleSize)
plt.savefig(generalPath / "NoOfMatches.jpg")




plt.close('all')
    




# idx_int = 1;
# for idx = 1:numel(fieldnames(data))
#     win_temp = data.(players{idx}).results.no_of_wins;
#     loss_temp = data.(players{idx}).results.no_of_losses;
#     noOfMatches = win_temp + loss_temp;
#     axisMatches{idx_int} = data.(players{idx}).name;
#     dataMatches(idx_int) = noOfMatches;
# 	idx_int = idx_int+1;
    
# end
    
# % [row_sort, indexes] = sortrows(win_data', 'Descend');
# [row_sort, indexes] = sortrows(dataMatches');
# row_sort = flip(row_sort);
# indexes = flip(indexes);
# for i = 1:size(dataMatches,2)
#     axisMatchesSort{i} = axisMatches{indexes(i)};
# end
# gcf = figure(idx_fig);
# hold on; box on; grid on;
# set(gcf, 'name', 'Numero di partite giocate');
# set(gcf, 'Units', 'Normalized', 'Position', [0.05, 0.05, 0.8, 0.8]);
# set(gcf, 'name', 'Partite giocate');
# bar(row_sort);
# set(gca, 'xtick', [1:length(axisMatchesSort)], 'xticklabel', ...
#     axisMatchesSort, 'xticklabelrotation', 90);
# xlim([0, max(size(axisMatchesSort))+1]);
# set(gca, 'ytick', [0:1:max(row_sort)]);
# filename = '..\Figures\_global';
# if not(exist(filename, 'dir'))
#     mkdir(filename);
# end
# filename = [filename, '\NumeroPartite'];
# print(filename, '-dpng','-r200');
