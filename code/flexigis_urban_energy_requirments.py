"""Module II.

Created on Wed Sep 13 12:38:36 2019

@author: AlAlha
"""
# TODO: generate log file
from __future__ import division
# import datetime
import pandas as pd
# import csv
import numpy as np
import matplotlib.pyplot as plt
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Configuration
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
Weather = True
SLP = True
EUIx = True
Ag = True
Co = True
Ed = True
In = True
Re = True
Hi = True
load_all = True
PV_all = True
Plot = True
input_destination_1 = "../data/01_raw_input_data/"
input_destination_2 = "../data/02_urban_output_data/"
output_destination = "../data/03_urban_energy_requirements/"
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Read Solar data
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if Weather is True:
    print('Weather Data Soda')
    soda = pd.read_csv(input_destination_1+'weather-data.csv',
                       encoding="ISO-8859-1", delimiter=',')
    GHI = soda['Global Horiz']/1000  # convert to kWh/m2
    wind = soda['Wind speed']
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Read Standard Load Profiles
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if SLP is True:
    print('Read and Normalise Standard Load Profiles')
    # , index_col='Zeitstempel', parse_dates=['Zeitstempel'])
    dfs = pd.read_csv(input_destination_1+'SLP.csv', delimiter=',')
    Zeit_stempel = dfs['Zeitstempel']
    AL = dfs['L0']/1000  # AL=aggricultural load
    CL = dfs['G0']/1000  # CL=commercial load
    EL = dfs['G1']/1000  # EL=educational load
    IL = dfs['G3']/1000  # IL=industrial load
    RL = dfs['H0']/1000  # CL=residential load
    SL = dfs['SB2']/1000  # SL=Street Light
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Read Electricity Usage Index kwh/m2 per year
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if EUIx is True:
    print('Read Electricity Usage Index kwh/m2 per year')
    x_a = 120/1000*1.0  # EUI_a
    x_c = 201/1000*1.0  # EUI_c
    x_e = 142/1000*1.0  # EUI_e
    x_i = 645/1000*1.0  # EUI_i
    x_r = 146/1000*1.0  # EUI_r
    x_sl = 4/1000  # EUIsl
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Simulate quarter load
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if Ag is True:
    print('Simulate Agr. quarter hourly Energy Requirments REs')
    dfa = pd.read_csv(input_destination_2+'agricultural.csv', delimiter=',')
    area_a = dfa['area'].sum()
    area_a_pv = area_a*0.267
    load_a = []
    fname = open(output_destination+'a_load.csv', 'w')
    fname.write('TIME;Load[kWh];PV[kWh]\n')
    for i, row in dfs.iterrows():
        row = str(Zeit_stempel[i]) + ';' + str(area_a*AL[i]*x_a) + \
            ';' + str(area_a_pv*GHI[i]*0.15*0.75) + '\n'
        load_a.append(row)
    fname.writelines(load_a)
    fname.close()
#    df1 = pd.read_csv('a_load.csv', delimiter=";")
#    df1['Load[kWh]'].plot()
#    df1['PV[kWh]'].plot()
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if Co is True:
    print('Simulate Com. quarter hourly Energy Requirments REs')
    dfc = pd.read_csv(input_destination_2+'commercial.csv', delimiter=',')
    area_c = dfc['area'].sum()
    area_c_pv = area_c*0.267
    load_c = []
    fname = open(output_destination+'c_load.csv', 'w')
    fname.write('TIME;Load[kWh];PV[kWh]\n')
    for i, row in dfs.iterrows():
        row = str(Zeit_stempel[i]) + ';' + str(area_c*CL[i]*x_c) + \
            ';' + str(area_c_pv*GHI[i]*0.15*0.75) + '\n'
        load_c.append(row)
    fname.writelines(load_c)
    fname.close()
#    df2 = pd.read_csv('c_load.csv', delimiter=";")
#    df2['Load[kWh]'].plot()
#    df2['PV[kWh]'].plot()
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if Ed is True:
    print('Simulate edu. quarter hourly Energy Requirments REs')
    dfe = pd.read_csv(input_destination_2+'educational.csv', delimiter=',')
    area_e = dfe['area'].sum()
    area_e_pv = area_e*0.267
    load_e = []
    fname = open(output_destination+'e_load.csv', 'w')
    fname.write('TIME;Load[kWh];PV[kWh]\n')
    for i, row in dfs.iterrows():
        row = str(Zeit_stempel[i]) + ';' + str(area_e*EL[i]*x_e) + \
            ';' + str(area_e_pv*GHI[i]*0.15*0.75) + '\n'
        load_e.append(row)
    fname.writelines(load_e)
    fname.close()
#    df3 = pd.read_csv('e_load.csv', delimiter=";")
#    df3['Load[kWh]'].plot()
#    df3['PV[kWh]'].plot()
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if In is True:
    print('Simulate Ind. quarter hourly Energy Requirments REs')
    dfi = pd.read_csv(input_destination_2+'industrial.csv', delimiter=',')
    area_i = dfi['area'].sum()
    area_i_pv = area_i*0.267
    load_i = []
    fname = open(output_destination+'i_load.csv', 'w')
    fname.write('TIME;Load[kWh];PV[kWh]\n')
    for i, row in dfs.iterrows():
        row = str(Zeit_stempel[i]) + ';' + str(area_i*IL[i]*x_i) + \
            ';' + str(area_i_pv*GHI[i]*0.15*0.75) + '\n'
        load_i.append(row)
    fname.writelines(load_i)
    fname.close()
#    df4 = pd.read_csv('i_load.csv', delimiter=";")
#    df4['Load[kWh]'].plot()
#    df4['PV[kWh]'].plot()
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if Re is True:
    print('Simulate Res. quarter hourly Energy Requirments REs')
    dfr = pd.read_csv(input_destination_2+'residential.csv', delimiter=',')
    area_r = dfr['area'].sum()
    area_r_pv = area_r*0.578
    load_r = []
    fname = open(output_destination+'r_load.csv', 'w')
    fname.write('TIME;Load[kWh];PV[kWh]\n')
    for i, row in dfs.iterrows():
        row = str(Zeit_stempel[i]) + ';' + str(area_r*RL[i]*x_r) + \
            ';' + str(area_r_pv*GHI[i]*0.15*0.75) + '\n'
        load_r.append(row)
    fname.writelines(load_r)
    fname.close()
#    df5 = pd.read_csv('r_load.csv', delimiter=";")
#    df5['Load[kWh]'].plot()
#    df5['PV[kWh]'].plot()
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if Hi is True:  # highway
    print('Simulate Urban Streetlightning. quarter hourly')
    dfsl = pd.read_csv(input_destination_2+'highway.csv', delimiter=',')
    area_sl = dfsl['area'].sum()
    no_building = len(dfsl)
    load_sl = []
    fname = open(output_destination+'sl_load.csv', 'w')
    fname.write('TIME;Load[kWh]\n')
    for i, row in dfs.iterrows():
        row = str(Zeit_stempel[i]) + ';' + str(area_sl*SL[i]*x_sl) + '\n'
        load_sl.append(row)
    fname.writelines(load_sl)
    fname.close()
#    df6 = pd.read_csv('sl_load.csv', delimiter =";")
#    df6['Load[kWh]'].plot()
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if PV_all is True:
    print('Aggrgate all simulated PV power generation')
    df1a = pd.read_csv(output_destination+'a_load.csv', delimiter=";")
    df2c = pd.read_csv(output_destination+'c_load.csv', delimiter=";")
    df3e = pd.read_csv(output_destination+'e_load.csv', delimiter=";")
    df4i = pd.read_csv(output_destination+'i_load.csv', delimiter=";")
    df5r = pd.read_csv(output_destination+'r_load.csv', delimiter=";")
    sum_pv_all = df1a['PV[kWh]'] / 1000 + df2c['PV[kWh]']\
        / 1000 + df3e['PV[kWh]'] / 1000 + df4i['PV[kWh]'] / 1000 +\
        df5r['PV[kWh]'] / 1000
    sum_pv = np.array(sum_pv_all)
    dfallpv = pd.DataFrame(sum_pv, columns=["PV[MWh]"])
    dfallpv.to_csv(output_destination+'Aggregated-pv.csv', index=True,
                   encoding='utf-8')  # , delimiter = ";" )
    print('Done! Thanx Alaa')
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if load_all is True:
    print('Aggrgate all simulated electricity consumptions')
    df11a = pd.read_csv(output_destination+'a_load.csv', delimiter=";")
    df21c = pd.read_csv(output_destination+'c_load.csv', delimiter=";")
    df31e = pd.read_csv(output_destination+'e_load.csv', delimiter=";")
    df41i = pd.read_csv(output_destination+'i_load.csv', delimiter=";")
    df51r = pd.read_csv(output_destination+'r_load.csv', delimiter=";")
    df61sl = pd.read_csv(output_destination+'sl_load.csv', delimiter=";")
    sum_load_all = (df11a['Load[kWh]'] + df21c['Load[kWh]'] +
                    df31e['Load[kWh]'] + df41i['Load[kWh]'] +
                    df51r['Load[kWh]'] + df61sl['Load[kWh]']) / 1000
    sum_load = np.array(sum_load_all)
    dfallload = pd.DataFrame(sum_load, columns=["Load[MWh]"])
    dfallload.to_csv(output_destination+'Aggregated-load.csv')
    print('Done! Thanx Alaa')
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# Simulate quarter load
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if Plot is True:
    print('Plot Urban Energy Requirments REs')
    dfsim_s = pd.read_csv(output_destination+'Aggregated-pv.csv',
                          delimiter=",")
    dfsim_s['PV[MWh]'].plot(style='r', figsize=(16, 8), grid=True)
    dfsim_l = pd.read_csv(output_destination+'Aggregated-load.csv',
                          delimiter=",")
    dfsim_l['Load[MWh]'].plot(style='g', figsize=(16, 8), grid=True)
    plt.xlabel('Time')
    plt.ylabel('MW')
    plt.title('Aggregated Energy Requirments in Oldenburg')
    plt.legend(['Simulated PV', 'Simulated load'], loc='upper left')
    plt.savefig("../data/04_Visualisation/Energy_Requirments_in_Oldenburg.png",
                dpi=300)
    plt.show()
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
