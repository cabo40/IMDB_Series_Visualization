# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 00:34:53 2020

@author: cfso1
"""

#load libraries
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import argparse

from imdb import IMDb

def IMDB_series_plotter(input_series, output, cmap, dpi=150):
    # create an instance of the IMDb class
    ia = IMDb()
    
    #Search for the series or IMDB_ID
    try:
        int(input_series)
        series = ia.get_movie(input_series)
    except:
        res = ia.search_movie(input_series)    
        series = ia.get_movie(res[0].movieID)
    
    try:
        ia.update(series, 'episodes')
    except:
        print("The input argument was not found to be a series")
        raise Exception('NotASeries')
        
    rating = []
    votes = []
    
    #Iterate over chapters and seasons to get the rating and votes
    for season, chapters in sorted(series['episodes'].items()):
        if season < 1:
            continue
        temp_rating = []
        temp_votes = []
        for chapter, descr in sorted(chapters.items()):
            try:
                temp_rating.append(descr['rating'])
            except:
                temp_rating.append(np.nan)
            try:
                temp_votes.append(descr['votes'])
            except:
                temp_votes.append(np.nan)
        rating.append(temp_rating)
        votes.append(temp_votes)
    
    #Convert the arrays to np.array filling the voids with nan
    np_rating = np.empty((len(rating),max([len(x) for x in rating])))
    np_votes = np.empty_like(np_rating)
    np_rating[:] = np.nan
    np_votes[:] = np.nan
    for i, season in enumerate(rating):
        for j, f_rating in enumerate(season):
            np_rating[i,j]=f_rating
            np_votes[i,j]=votes[i][j]
    
    #Convert broken ratings to nan
    np_rating[np_rating==12345678910.0]=np.nan
    
    #Remove last seasons with no chapters rated
    while np.all(np.isnan(np_rating[-1,:])):
        np_rating = np_rating[:-1, :]
    
    #Add sequential info about season and chapter
    np_rating = np.insert(np_rating, 0, np.arange(1,np_rating.shape[1]+1), axis=0)
    np_rating = np.insert(np_rating, 0, np.arange(0,np_rating.shape[0]), axis=1)
    np_rating[0,0] = np.nan
    np_rating = np.transpose(np_rating)
    
    np_votes = np.insert(np_votes, 0, np.arange(1,np_votes.shape[1]+1), axis=0)
    np_votes = np.insert(np_votes, 0, np.arange(0,np_votes.shape[0]), axis=1)
    np_votes[0,0] = np.nan
    
    #Start plot process 
    f, ax = plt.subplots(figsize=(np_rating.shape[1], np_rating.shape[0]))
    
    #We will mask the slots where there's no chapter or no rating
    mask = np.zeros_like(np_rating, dtype=np.bool)
    
    mask[np.isnan(np_rating)]= True
    mask[1:,0] = False
    mask[0,1:] = False
    
    #This heatmap is actually the chapter and season counter
    sns.heatmap(np_rating,
                mask = mask,
                square = True,
                linewidths = 10,
                cbar=False,
                cmap = 'Greys',
                vmin = -100,
                vmax = 1,
                annot = True,
                annot_kws = {'size': 12},
                zorder=1)
    
    mask[:,0] = True
    mask[0,:] = True
    
    #User defined colormap or default to RdYlGn
    if not cmap: cmap = 'RdYlGn'
        
    sns.heatmap(np_rating,
                mask = mask,
                square = True,
                linewidths = 10,
                cbar=False,
                cmap = cmap,
                vmin = 6.8,
                vmax = 9.2,
                annot = True,
                annot_kws = {'size': 12},
                zorder=2)
  
    
    ax.set_title(series['long imdb title'],fontsize=24)
    ax.set_ylabel('Chapter', fontsize=18)
    ax.set_xlabel('Season', fontsize=18)
    ax.xaxis.set_label_position('top') 
    
    #We remove the axis ticks from the plot
    ax.set_xticks([])
    ax.set_yticks([])
    
    #And save the plot
    # plt.savefig(res[0]['long imdb title'].replace(" ",
    #                                               "_").replace("\"",
    #                                                            ""), dpi=dpi)
    plt.savefig(output, dpi=dpi)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input', type=str, help='An IMDB ID for a series or the name of a series')
    parser.add_argument(
        '-o', '--output', type=str, help='The output path for the plot, can be relative or absolute')
    parser.add_argument(
        '-c', '--cmap', type=str, help='(Optional) The Matplotlib colormap to use')
    args = parser.parse_args()
    IMDB_series_plotter(args.input, args.output, args.cmap)
