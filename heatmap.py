#!/usr/bin/env python3.9
# coding: utf-8

import pandas as pd
import matplotlib.pyplot as plt
import seaborn
# import re
# import os
from datetime import datetime
import sys

def generate_heatmap():
    """
        Cleo Pinoli has written this code to generate a heatmap
    """
    #Attivita_L = "./output/select_all_from_attivita.csv"
    Attivita_L = str(sys.argv[1])
    # Etichette1018 = "./output/preparedLabelsForHeatmap.csv"
    Etichette1018 = str(sys.argv[2])

    #NOTE: last time i ran this, i changed all "nometransizione" into "nomeattivita", be aware of that :) cheers

    logsDf = pd.read_csv(Attivita_L)
    logsDf.insert(4, 'Cluster', value = 0, allow_duplicates=False)
    # fill the new column with the cluster from which the log was taken, basically
    etichetteDf = pd.read_csv(Etichette1018)
    etichetteDf.sort_values(by=['ClusterId'], inplace=True, ignore_index=True)

    logsDf['NomeLog']=logsDf['NomeLog'].str.replace(r'.xes', '', regex=True)
    for i in range(len(logsDf)):
        for j in range(len(etichetteDf)):
            if logsDf.at[i, 'NomeLog'] == etichetteDf.at[j, 'NomeLog']:
                value = etichetteDf.at[j, 'ClusterId']
                logsDf.at[i, 'Cluster'] = value

    grouped_activities_dict = {}
    grouped_activities_dict = logsDf.groupby('Cluster')['NomeAttivita'].unique() 
    dict((grouped_activities_dict))
    for key in grouped_activities_dict.keys():
        grouped_activities_dict[key] = grouped_activities_dict[key]

    sets_df = pd.DataFrame(grouped_activities_dict)
    #LIAR, it's a lists_df

    NO_OF_CLUSTERS = len(sets_df)

    activities_lists_dict = {}
    print(sets_df.keys())

    for i in range (len(sets_df)): # numero cluster: i
        for j in range (len(sets_df.at[i,'NomeAttivita'])): #numero attivita: j
            if sets_df.at[i, 'NomeAttivita'][j] in activities_lists_dict:
                activities_lists_dict[sets_df.at[i, 'NomeAttivita'][j]].append(i)
            else:
                activities_lists_dict[sets_df.at[i, 'NomeAttivita'][j]]=[] # add the new key x value pair
                activities_lists_dict[sets_df.at[i, 'NomeAttivita'][j]].append(i)

    # we currently have a dictionary of activity x (list of clusters)

    activities_lists_dict2 = {}

    for k in activities_lists_dict.keys():
        if len(activities_lists_dict[k]) in activities_lists_dict2:
            activities_lists_dict2[len(activities_lists_dict[k])].append(k)
        else:
            activities_lists_dict2[len(activities_lists_dict[k])] = []
            activities_lists_dict2[len(activities_lists_dict[k])].append(k)

    final_activities_list = []
    for key in sorted(activities_lists_dict2):
        for a in range(len(activities_lists_dict2[key])):
            final_activities_list = [activities_lists_dict2[key][a]] + final_activities_list

    df_mapping = pd.DataFrame(final_activities_list) #{'list': activities_list}
    #sort_mapping = df_mapping.reset_index().set_index('list')
    dict1 = df_mapping.to_dict()
    dict2 = dict1[0]

    def get_key(val):
        for key, value in dict2.items():
             if val == value:
                    return key
     
        return 99 #what do i return if the activity is NOT there? Note that I cannot use '0' as it is an index.

    #"quando ho scritto questo codice, soltanto io e Dio sapevamo cosa facesse. Ora lo sa solo Dio."

    logsDf['ordine'] = 0
    for i in range (len(logsDf)):
        logsDf.at[i, 'ordine'] = get_key(logsDf.at[i, 'NomeAttivita'])

    logsDf.sort_values(by=['ordine'], inplace=True)


    cluster_edges_list = []
    clusterid = etichetteDf.columns.values.tolist()[1].strip("'")

    for i in range(len(etichetteDf)-1):
        if etichetteDf.at[i, clusterid] == etichetteDf.at[i+1, clusterid]:
            pass
        else:
            cluster_edges_list.append(i+1)

    logs_list = etichetteDf['NomeLog']
    all_activities_list = logsDf['NomeAttivita'].unique()
    output_df = pd.DataFrame(columns=final_activities_list, index=logs_list)
    output_df = output_df.fillna(0)
    output_df

    len(logsDf)

    for j in range (len(logsDf)):
        if logsDf.at[j,'NomeLog'].strip("'") in output_df.index and logsDf.at[j, 'NomeAttivita'].strip("'") in final_activities_list:
            row = logsDf.at[j,'NomeLog']
            col = logsDf.at[j, 'NomeAttivita']
            if logsDf.at[j, 'IsRepeating'] == 0:
                output_df.loc[row, col] = 0.5 #will change colors on this 
            else:
                if logsDf.at[j, 'IsRepeating'] == 1:
                    output_df.loc[row, col] = 1

    plt.figure(figsize=(200, 200))

    ax = seaborn.heatmap(output_df)
    ax.hlines(cluster_edges_list, *ax.get_xlim())

    # heatmap_folder = os.getenv('HEATMAP_FOLDER')
    # plt.savefig(f"{heatmap_folder}/{datetime.now().time()}.png")
    plt.savefig(f"./heatmaps/Heatmap{datetime.now().strftime('%d_%b_%H_%M')}.png")

if __name__ == "__main__":
    generate_heatmap()
