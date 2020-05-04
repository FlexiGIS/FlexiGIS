"""**This module simulates Urban Energy Requirements**.

Outputs are stored stored as csv.
"""
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
import logging

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',
                    filename="../code/log/flexigis_urban_energy.log",
                    level=logging.DEBUG)


class UrbanEnergyRequirement:
    """Simulate urban energy requirements.

    :returns: csv files of simulated load profile and PV requirements
    """

    def __init__(self):
        """Init function."""
        self.input_destination_1 = "../data/01_raw_input_data/"
        self.input_destination_2 = "../data/02_urban_output_data/"
        self.output_destination = "../data/03_urban_energy_requirements/"
        self.output_destination2 = "../data/04_Visualisation/"
        self.norm = 1000
        self.factorGHI = 0.15*0.75
        if Path(self.output_destination).exists():
            logging.info("directory {} already exists.".
                         format("03_urban_energy_requirements"))
            pass
        else:
            os.mkdir(self.output_destination)
            logging.info("directory {} succesfully created!.".
                         format("03_urban_energy_requirements"))
# if Weather is True:

    def weather(self):
        """Read solar data."""
        print('Weather Data: Solar Radiation Data')
        logging.info("read weather data Soda")
        soda = pd.read_csv(self.input_destination_1+'weather-data.csv',
                           encoding="ISO-8859-1", delimiter=',')
        self.GHI = soda['Global Horiz']/self.norm
        self.wind = soda['Wind speed']/self.norm

# if SLP is True:
    def standard_load_profiles(self):
        """Read Standard Load Profiles."""
        print('Read and Normalise Standard Load Profiles')
        logging.info("Read and Normalise Standard Load Profiles")
        # , index_col='Zeitstempel', parse_dates=['Zeitstempel'])
        self.dfs = pd.read_csv(self.input_destination_1+'SLP.csv',
                               delimiter=',')
        self.Zeit_stempel = self.dfs['Zeitstempel']
        self.AL = self.dfs['L0']/self.norm  # AL=aggricultural load
        self.CL = self.dfs['G0']/self.norm  # CL=commercial load
        self.EL = self.dfs['G1']/self.norm  # EL=educational load
        self.IL = self.dfs['G3']/self.norm  # IL=industrial load
        self.RL = self.dfs['H0']/self.norm  # CL=residential load
        self.SL = self.dfs['SB2']/self.norm  # SL=Street Light

# if EUIx is True:
    def electricity_usage_index(self):
        """Read Electricity Usage Index kwh/m2 per year."""
        print('Read Electricity Usage Index kwh/m2 per year')
        logging.info("Read Electricity Usage Index kwh/m2 per year")
        self.x_a = 120/self.norm  # EUI_a
        self.x_c = 201/self.norm  # EUI_c
        self.x_e = 142/self.norm  # EUI_e
        self.x_i = 645/self.norm  # EUI_i
        self.x_r = 146/self.norm  # EUI_r
        self.x_sl = 4/self.norm  # EUIsl

# if Ag is True:
    def agricultural_load(self):
        """Simulate quarter load."""
        print('Simulate Agr. quarter hourly Energy Requirments REs')
        dfa = gpd.read_file(self.input_destination_2 +
                            'agricultural/agricultural.shp')
        area_a = dfa['area'].sum()
        area_a_pv = area_a*0.267
        load_a = []
        fname = open(self.output_destination+'a_load.csv', 'w')
        fname.write('TIME;Load[kWh];PV[kWh]\n')

        for i, row in self.dfs.iterrows():
            row = str(self.Zeit_stempel[i]) + ';' + \
                str(area_a*self.AL[i]*self.x_a) + ';' + \
                str(area_a_pv*self.GHI[i]*self.factorGHI) + '\n'

            load_a.append(row)
        fname.writelines(load_a)
        fname.close()
    #    df1 = pd.read_csv('a_load.csv', delimiter=";")
    #    df1['Load[kWh]'].plot()
    #    df1['PV[kWh]'].plot()
        logging.info("Agr. quarter hourly Energy Requirments REs simulated.")

# if Co is True:
    def commercial_energy_req(self):
        """Simulate Com. quarter hourly Energy Requirments REs."""
        print('Simulate Com. quarter hourly Energy Requirments REs')
        dfc = gpd.read_file(self.input_destination_2 +
                            'commercial/commercial.shp')
        area_c = dfc['area'].sum()
        area_c_pv = area_c*0.267
        load_c = []
        fname = open(self.output_destination+'c_load.csv', 'w')
        fname.write('TIME;Load[kWh];PV[kWh]\n')

        for i, row in self.dfs.iterrows():
            row = str(self.Zeit_stempel[i]) + ';' + \
                str(area_c*self.CL[i]*self.x_c) + ';' + \
                str(area_c_pv*self.GHI[i]*self.factorGHI) + '\n'

            load_c.append(row)
        fname.writelines(load_c)
        fname.close()
    #    df2 = pd.read_csv('c_load.csv', delimiter=";")
    #    df2['Load[kWh]'].plot()
    #    df2['PV[kWh]'].plot()
        logging.info("Com. quarter hourly Energy Requirments REs simulated.")

# if Ed is True:
    def eductaional_energy_req(self):
        """Simulate edu. quarter hourly Energy Requirments REs."""
        print('Simulate edu. quarter hourly Energy Requirments REs')
        dfe = gpd.read_file(self.input_destination_2 +
                            'educational/educational.shp')
        area_e = dfe['area'].sum()
        area_e_pv = area_e*0.267
        load_e = []
        fname = open(self.output_destination+'e_load.csv', 'w')
        fname.write('TIME;Load[kWh];PV[kWh]\n')
        for i, row in self.dfs.iterrows():
            row = str(self.Zeit_stempel[i]) + ';' +\
                str(area_e*self.EL[i] * self.x_e) + ';' + \
                str(area_e_pv*self.GHI[i]*self.factorGHI) + '\n'
            load_e.append(row)
        fname.writelines(load_e)
        fname.close()
    #    df3 = pd.read_csv('e_load.csv', delimiter=";")
    #    df3['Load[kWh]'].plot()
    #    df3['PV[kWh]'].plot()
        logging.info("Edu. quarter hourly Energy Requirments REs simulated.")

# if In is True:
    def industrial_energy_req(self):
        """Simulate Ind. quarter hourly Energy Requirments REs."""
        print('Simulate Ind. quarter hourly Energy Requirments REs')
        dfi = gpd.read_file(self.input_destination_2 +
                            'industrial/industrial.shp')
        area_i = dfi['area'].sum()
        area_i_pv = area_i*0.267
        load_i = []
        fname = open(self.output_destination+'i_load.csv', 'w')
        fname.write('TIME;Load[kWh];PV[kWh]\n')
        for i, row in self.dfs.iterrows():
            row = str(self.Zeit_stempel[i]) + ';' +\
                str(area_i*self.IL[i] * self.x_i) + ';' +\
                str(area_i_pv*self.GHI[i]*self.factorGHI) + '\n'
            load_i.append(row)
        fname.writelines(load_i)
        fname.close()
    #    df4 = pd.read_csv('i_load.csv', delimiter=";")
    #    df4['Load[kWh]'].plot()
    #    df4['PV[kWh]'].plot()
        logging.info("Ind. quarter hourly Energy Requirments REs simulated.")

# if Re is True:
    def residential_energy_req(self):
        """Simulate Res. quarter hourly Energy Requirments REs."""
        dfr = gpd.read_file(self.input_destination_2 +
                            'residential/residential.shp')
        area_r = dfr['area'].sum()
        area_r_pv = area_r*0.578
        load_r = []
        fname = open(self.output_destination+'r_load.csv', 'w')
        fname.write('TIME;Load[kWh];PV[kWh]\n')
        for i, row in self.dfs.iterrows():
            row = str(self.Zeit_stempel[i]) + ';' +\
                str(area_r*self.RL[i] * self.x_r) + ';' +\
                str(area_r_pv*self.GHI[i]*self.factorGHI) + '\n'
            load_r.append(row)
        fname.writelines(load_r)
        fname.close()
    #    df5 = pd.read_csv('r_load.csv', delimiter=";")
    #    df5['Load[kWh]'].plot()
    #    df5['PV[kWh]'].plot()
        logging.info("Res. quarter hourly Energy Requirments REs simulated.")

# if Hi is True:  # highway
    def highway_energy_req(self):
        """Simulate Urban Streetlightning. quarter hourly."""
        print('Simulate Urban Streetlightning. quarter hourly')
        dfsl = gpd.read_file(self.input_destination_2+'highway/highway.shp')
        area_sl = dfsl['area'].sum()
        self.no_building = len(dfsl)
        load_sl = []
        fname = open(self.output_destination+'sl_load.csv', 'w')
        fname.write('TIME;Load[kWh]\n')
        for i, row in self.dfs.iterrows():
            row = str(self.Zeit_stempel[i]) + ';' + str(area_sl*self.SL[i] *
                                                        self.x_sl) + '\n'
            load_sl.append(row)
        fname.writelines(load_sl)
        fname.close()
    #    df6 = pd.read_csv('sl_load.csv', delimiter =";")
    #    df6['Load[kWh]'].plot()
        logging.info("Urban Streetlightning. quarter hourly simulated.")

# if PV_all is True:
    def PV_aggregate(self):
        """Aggrgate all simulated PV power generation."""
        print('Aggrgate all simulated PV power generation')
        df1a = pd.read_csv(self.output_destination+'a_load.csv', delimiter=";")
        df2c = pd.read_csv(self.output_destination+'c_load.csv', delimiter=";")
        df3e = pd.read_csv(self.output_destination+'e_load.csv', delimiter=";")
        df4i = pd.read_csv(self.output_destination+'i_load.csv', delimiter=";")
        df5r = pd.read_csv(self.output_destination+'r_load.csv', delimiter=";")
        sum_pv_all = (df1a['PV[kWh]'] + df2c['PV[kWh]'] + df3e['PV[kWh]'] +
                      df4i['PV[kWh]'] + df5r['PV[kWh]']) / self.norm
        sum_pv = np.array(sum_pv_all)
        dfallpv = pd.DataFrame(sum_pv, columns=["PV[MWh]"])
        dfallpv.to_csv(self.output_destination+'Aggregated-pv.csv', index=True,
                       encoding='utf-8')  # , delimiter = ";" )
        logging.info("All simulated PV power generation aggregated")
        print('Info: Aggt. PV Power')

# if load_all is True:
    def electricity_aggregate(self):
        """Aggrgate all simulated electricity consumptions."""
        print('Aggrgate all simulated electricity consumptions')
        df11a = pd.read_csv(self.output_destination+'a_load.csv',
                            delimiter=";")
        df21c = pd.read_csv(self.output_destination+'c_load.csv',
                            delimiter=";")
        df31e = pd.read_csv(self.output_destination+'e_load.csv',
                            delimiter=";")
        df41i = pd.read_csv(self.output_destination+'i_load.csv',
                            delimiter=";")
        df51r = pd.read_csv(self.output_destination+'r_load.csv',
                            delimiter=";")
        df61sl = pd.read_csv(self.output_destination+'sl_load.csv',
                             delimiter=";")
        sum_load_all = (df11a['Load[kWh]'] + df21c['Load[kWh]'] +
                        df31e['Load[kWh]'] + df41i['Load[kWh]'] +
                        df51r['Load[kWh]'] + df61sl['Load[kWh]']) / self.norm
        sum_load = np.array(sum_load_all)
        dfallload = pd.DataFrame(sum_load, columns=["Load[MWh]"])
        dfallload.to_csv(self.output_destination+'Aggregated-load.csv')
        logging.info("All ssimulated electricity consumptions aggregated")
        print('Info: Aggt. Electricity Load')

# if Plot is True:
    def plot_quarter_load_energy(self):
        """Simulate quarter load and plot Urban Energy Requirments REs."""
        print('Plot Urban Energy Requirments REs')
        fig_size = (14, 8)
        dfsim_s = pd.read_csv(self.output_destination+'Aggregated-pv.csv',
                              delimiter=",")
        dfsim_s['PV[MWh]'].plot(style='r', figsize=fig_size, grid=True)
        dfsim_l = pd.read_csv(self.output_destination+'Aggregated-load.csv',
                              delimiter=",")
        dfsim_l['Load[MWh]'].plot(style='g', figsize=fig_size, grid=True)
        plt.xlabel('Time')
        plt.ylabel('MW')
        plt.title('Aggregated Energy Requirments in Oldenburg')
        plt.legend(['Simulated PV', 'Simulated load'], loc='upper left')
        plt.savefig(self.output_destination2+"Energy_Requirments.png", dpi=300)
        plt.show()
        logging.info("Urban Energy Requirments REs plot generated succesfuly")

    def flexigis_urban_simulation(self, Weather=True, SLP=True, EUIx=True,
                                  Ag=True, Co=True, Ed=True, In=True, Re=True,
                                  Hi=True, load_all=True, PV_all=True,
                                  Plot=True):
        """Simulate urbanEnergy requirements for target city."""
        if Weather:
            self.weather()
        if SLP:
            self.standard_load_profiles()
        if EUIx:
            self.electricity_usage_index()
        if Ag:
            self.agricultural_load()
        if Co:
            self.commercial_energy_req()
        if Ed:
            self.eductaional_energy_req()
        if In:
            self.industrial_energy_req()
        if Re:
            self.residential_energy_req()
        if Hi:
            self.highway_energy_req()
        if PV_all:
            self.PV_aggregate()
        if load_all:
            self.electricity_aggregate()
        if Plot:
            self.plot_quarter_load_energy()


if __name__ == "__main__":
    flexigis_energy = UrbanEnergyRequirement()
    flexigis_energy.flexigis_urban_simulation()
