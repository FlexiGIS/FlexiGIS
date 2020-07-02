"""**This module simulates Urban Energy Requirements**.

Outputs are stored stored as csv.
"""
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path
import pickle
import logging

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',
                    filename="../code/log/demand_supply.log",
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
        self.norm = 1000  # standard unit converter
        if Path(self.output_destination).exists():
            pass
        else:
            os.mkdir(self.output_destination)

    def feedin_data(self):
        """Get wind and pv feed in data."""
        with open(os.path.join(self.input_destination_1, 'fp'), 'rb') as fp:
            feedin_parameter = pickle.load(fp)
        self.peak_power = feedin_parameter[0]  # in watts
        self.module_area = feedin_parameter[1]
        self.norminal_power_wind = feedin_parameter[2]  # in watts
        pv_feedin = pd.read_csv(os.path.join(
            self.input_destination_1, 'pv_power.csv'))
        wind_feedin = pd.read_csv(os.path.join(
            self.input_destination_1, 'wind_power.csv'))
        pv_feedin = pv_feedin.reindex()
        self.time_stamp = pv_feedin[['time']]
        self.pv_data = pv_feedin["pv"]
        self.wind_power_data = wind_feedin["wind"]
        logging.info("Feedin data and powersystem parameter imported.")
        print('*** Feedin data imported ***')

    def standard_load_profiles(self):
        """Read Standard Load Profiles."""
        self.dfs = pd.read_csv(os.path.join(
            self.input_destination_1, 'SLP.csv'))
        # get different scenario load profiles in kWh
        self.AL, self.CL = self.dfs['L0']/self.norm, self.dfs['G0']/self.norm
        self.EL, self.IL = self.dfs['G1']/self.norm, self.dfs['G3']/self.norm
        self.RL, self.SL = self.dfs['H0']/self.norm, self.dfs['SB2']/self.norm
        logging.info("Get load profile for different scenarios.")
        print('Info: Load profile data imported')

    def electricity_usage_index(self):
        """Calculate Electricity Usage Index for different building type kWh/m2 per year."""
        self.x_a, self.x_c = 120/self.norm, 201/self.norm
        self.x_e, self.x_i = 142/self.norm, 645/self.norm
        self.x_r, self.x_sl = 146/self.norm, 4/self.norm
        logging.info(
            "Calculate electricty usage index for urban infrastructure.")
        print('Info: Electricity usage index calculated')

    def roofTop_pv_capacity(self):
        """Calculate maximum installed pv capacity as a function of rooftop area."""
        dfa = gpd.read_file(os.path.join(
            self.input_destination_2, 'agricultural/agricultural.shp'))
        dfc = gpd.read_file(os.path.join(
            self.input_destination_2, 'commercial/commercial.shp'))
        dfe = gpd.read_file(os.path.join(
            self.input_destination_2, 'educational/educational.shp'))
        dfi = gpd.read_file(os.path.join(
            self.input_destination_2, 'industrial/industrial.shp'))
        dfr = gpd.read_file(os.path.join(
            self.input_destination_2, 'residential/residential.shp'))
        self.area_a, self.area_c = dfa['area'].sum(), dfc['area'].sum()
        self.area_e, self.area_i = dfe['area'].sum(), dfi['area'].sum()
        self.area_r = dfr['area'].sum()
        self.area_a_pv, self.area_c_pv = self.area_a*0.267, self.area_c*0.267
        self.area_e_pv, self.area_i_pv = self.area_e*0.267, self.area_i*0.267
        self.area_r_pv = self.area_r*0.578
        # calculate aggregate peak power at rooftop
        total_roof_to_area = self.area_a_pv+self.area_c_pv + \
            self.area_e_pv+self.area_i_pv+self.area_r_pv
        self.peak_power_agg = (
            self.peak_power*(total_roof_to_area/self.module_area)) / self.norm  # KW
        print('Info: Maximum installed pv capacity = {} KW'.format(
            str(self.peak_power_agg)))
        # KW TODO: proper calculate max. installed cpacity for wind
        max_installed_wind_power = 305000
        maximum_capacity = [max_installed_wind_power, self.peak_power_agg]
        with open(os.path.join(self.output_destination, 'mc'), 'wb') as mc:
            pickle.dump(maximum_capacity, mc)
        logging.info("Calculate maximum installed PV capacity at roof top.")

    def agricultural_load(self):
        """Simulate Agricultural building type electricity demand and PV feedin supply."""
        load_a = self.time_stamp
        load_a['Load[kWh]'] = self.AL*self.area_a*self.x_a
        load_a['PV[kWh]'] = (self.pv_data*self.peak_power *
                             (self.area_a_pv/self.module_area)) / self.norm  # kWh
        load_a.to_csv(os.path.join(self.output_destination, 'a_load.csv'))
        logging.info(
            "Calculate electricty demand and supply for agricultural buildings")
        print('Info: Agricultural building load and pv supply simulation.')

    def commercial_energy_req(self):
        """Simulate Com.  building type electricity demand and PV feedin supply."""
        load_c = self.time_stamp
        load_c['Load[kWh]'] = self.CL*self.area_c*self.x_c
        load_c['PV[kWh]'] = (self.pv_data*self.peak_power *
                             (self.area_c_pv/self.module_area))/self.norm
        load_c.to_csv(os.path.join(self.output_destination, 'c_load.csv'))
        logging.info(
            "Calculate electricty demand and supply for commercial buildings")
        print('Info: Commercial building load and pv supply siml.')

    def eductaional_energy_req(self):
        """Simulate edu. quarter hourly Energy Requirments REs."""
        load_e = self.time_stamp
        load_e['Load[kWh]'] = self.EL*self.area_e*self.x_e
        load_e['PV[kWh]'] = (self.pv_data*self.peak_power *
                             (self.area_e_pv/self.module_area))/self.norm
        load_e.to_csv(os.path.join(self.output_destination, 'e_load.csv'))
        logging.info(
            "Calculate electricty demand and supply for educational buildings")
        print('Info: Eductaional building load and pv supply siml.')

    def industrial_energy_req(self):
        """Simulate Ind. quarter hourly Energy Requirments REs."""
        load_i = self.time_stamp
        load_i['Load[kWh]'] = self.IL*self.area_i*self.x_i
        load_i['PV[kWh]'] = (self.pv_data*self.peak_power *
                             (self.area_i_pv/self.module_area))/self.norm
        load_i.to_csv(os.path.join(self.output_destination, 'i_load.csv'))
        logging.info(
            "Calculate electricty demand and supply for industrial buildings")
        print('Info: Industrial building load and pv supply siml.')

    def residential_energy_req(self):
        """Simulate Res. quarter hourly Energy Requirments REs."""
        load_r = self.time_stamp
        load_r['Load[kWh]'] = self.RL*self.area_r*self.x_r
        load_r['PV[kWh]'] = (self.pv_data*self.peak_power *
                             (self.area_r_pv/self.module_area))/self.norm
        load_r.to_csv(os.path.join(self.output_destination, 'r_load.csv'))
        logging.info(
            "Calculate electricty demand and supply for residential buildings")
        print('Info: Residential building load and pv supply siml.')

    def highway_energy_req(self):
        """Simulate Urban Streetlightning. quarter hourly."""
        street_data = gpd.read_file(os.path.join(
            self.input_destination_2, 'highway/highway.shp'))
        area_sl = street_data['area'].sum()
        self.no_building = len(street_data)
        load_sl = self.time_stamp
        load_sl['Load[kWh]'] = self.SL*area_sl*self.x_sl
        load_sl.to_csv(os.path.join(self.output_destination, 'sl_load.csv'))
        logging.info(
            "Calculate electricty demand for street lights")
        print('Info: Streetlightning load siml.')

    def aggregate_demand_supply(self):
        """Aggrgate all simulated PV power generation."""
        print('Info: Aggregate simulated PV power generation and electricity demand.')

        demand_supply_agri = pd.read_csv(
            os.path.join(self.output_destination, 'a_load.csv'))
        demand_supply_comm = pd.read_csv(
            os.path.join(self.output_destination, 'c_load.csv'))
        demand_supply_educ = pd.read_csv(
            os.path.join(self.output_destination, 'e_load.csv'))
        demand_supply_indu = pd.read_csv(
            os.path.join(self.output_destination, 'i_load.csv'))
        demand_supply_resi = pd.read_csv(
            os.path.join(self.output_destination, 'r_load.csv'))
        demand_street_light = pd.read_csv(
            os.path.join(self.output_destination, 'sl_load.csv'))

        # aggregate all pv supply for the different building types
        agg_pv = (demand_supply_agri['PV[kWh]'] + demand_supply_comm['PV[kWh]'] +
                  demand_supply_educ['PV[kWh]'] + demand_supply_indu['PV[kWh]'] +
                  demand_supply_resi['PV[kWh]'])/self.norm  # to MWh
        agg_pv = np.array(agg_pv)
        agg_pv = pd.DataFrame(agg_pv, columns=["PV[MWh]"])

        # aggregate all electricity demand for the different building types (MWh)
        agg_load = (demand_supply_agri['Load[kWh]'] + demand_supply_comm['Load[kWh]'] +
                    demand_supply_educ['Load[kWh]'] + demand_supply_indu['Load[kWh]'] +
                    demand_supply_resi['Load[kWh]'] + demand_street_light['Load[kWh]'])/self.norm

        # prepare demand and supply data for optimization
        agg_load = np.array(agg_load)
        agg_load = pd.DataFrame(agg_load, columns=["Load[MWh]"])
        agg_load['PV[MWh]'] = agg_pv["PV[MWh]"]
        agg_load['demand_el'] = agg_load["Load[MWh]"].values * \
            1000  # Kilo-watts hour
        agg_load['wind'] = self.wind_power_data  # normalized wind feedin data
        agg_load['pv'] = self.pv_data  # normalized pv feedin data
        agg_load['time'] = self.time_stamp['time']
        agg_load = agg_load.set_index('time')

        agg_load.loc[:, ["Load[MWh]", 'PV[MWh]']].to_csv(os.path.join(
            self.output_destination, 'aggregated-demand-supply.csv'))
        agg_load.loc[:, ["demand_el", 'wind', 'pv']].to_csv(
            os.path.join(self.output_destination, 'optimization-commodities.csv'))
        logging.info(
            "Calculate aggregated electricty demand and supplies")

    def plot_quarter_load_energy(self):
        """Simulate quarter load and plot Urban Energy Requirments REs."""
        print('Info: Plot Urban Energy Requirments.')
        fig_size = (14, 8)
        sim_df = pd.read_csv(os.path.join(
            self.output_destination, 'aggregated-demand-supply.csv'))
        sim_df['PV[MWh]'].plot(style='r', figsize=fig_size, grid=True)
        sim_df['Load[MWh]'].plot(style='g', figsize=fig_size, grid=True)
        plt.xlabel('Time')
        plt.ylabel('MW')
        plt.title('Aggregated Energy Requirments in Oldenburg')
        plt.legend(['Simulated PV', 'Simulated load'], loc='upper left')
        plt.savefig(self.output_destination2+"Energy_Requirments.png", dpi=300)
        plt.show()
        logging.info("Generate demand and supply plot")

    def flexigis_urban_simulation(self):
        """Simulate urban Energy requirements for target location."""
        self.feedin_data()
        self.standard_load_profiles()
        self.electricity_usage_index()
        self.roofTop_pv_capacity()
        self.agricultural_load()
        self.commercial_energy_req()
        self.eductaional_energy_req()
        self.industrial_energy_req()
        self.residential_energy_req()
        self.highway_energy_req()
        self.aggregate_demand_supply()
        self.plot_quarter_load_energy()
        logging.info("Electricity Demand and Supply simulation Done!")


if __name__ == "__main__":
    flexigis_energy = UrbanEnergyRequirement()
    flexigis_energy.flexigis_urban_simulation()
