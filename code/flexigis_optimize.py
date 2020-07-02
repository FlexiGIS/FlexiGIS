'''This script is use to derive optimal RE feedin capacity and also the optimal
storage required for an energy system. The optimisation is carried out using
the oemof solph package. The below codes are taken from the `oemof-example`_ codes 
github repository. The optimization settings are described below by the following parameters:

- optimize wind, pv, gas_resource and storage
- set investment cost for wind, pv and storage
- set gas price for kWh

See link here: `oemof-example`_
'''
import pandas as pd
import os
import pprint as pp
# import datetime
import matplotlib.pyplot as plt
import pickle
import logging
from oemof.tools import economics
import oemof.solph as solph
from oemof.outputlib import processing, views
import oemof.outputlib as outputlib
import oemof_visio as oev
from flexigis_utils import shape_legend


logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',
                    filename="../code/log/optimize.log",
                    level=logging.DEBUG)


# load demand and supply data
def get_commodities(data_path,
                    filename='optimization-commodities.csv'):
    """Import simulated urban electricty demand and feedin data.

    :pandas dataframe:  data: with hourly resolution as index
    """
    data = pd.read_csv(os.path.join(data_path, filename),
                       index_col='time', parse_dates=True)
    # check whether datetime index is naive or localize
    if data.index.tzinfo is not None and \
            data.index.tzinfo.utcoffset(data.index) is not None:
        # convert to premitive UTC time
        data = data.tz_convert(None)
    logging.info("Feedin data and powersystem parameter imported.")
    return data


# get the maximum install pv capacity at roof top
def get_installed_pv_capacity(dir_path_1):
    """Get maximum installed capacity calculated based on urban infrastructure.

    :list: maximum_capacity: len(maximum_capacity) = 3
    """
    with open(os.path.join(dir_path_1, 'mc'), 'rb') as mc:
        maximum_capacity = pickle.load(mc)
    logging.info("Get power system parameters.")
    return maximum_capacity


# Create oemof energy system
def oemof_power_system(data, dir_path_2, nominal_value_gas, variable_cost_gas,
                       max_cap_pv, max_cap_wind, inst_pv_cap, inst_wind_cap):
    """Creates an oemof energy system model and optimizes the investment of
    flexibilty technology.

    :dataframe: data: demand, normalized pv and windpower timeseries
    :string: dir_path_2: directory path, to temporary dump optimization results
    :float or int: nominal_value_gas
    :float or int: variable_cost_gas: float
    :float or int: max_cap_pv: maximum pv capacity
    :float or int: max_cap_wind: maximum wind capacity
    :float or int: inst_pv_cap: existing installed pv capacity
    :float or int: inst_wind_cap: existing installed windpower capacity
    """
    # create an energy system using setting defualt economic parameters
    number_timesteps = len(data.index)
    period = data.index.year[10]
    date_time_index = pd.date_range('1/1/'+str(period),
                                    periods=number_timesteps,
                                    freq='H')
    energysystem = solph.EnergySystem(timeindex=date_time_index)
    # Calculate investment of technologies using oemof's economic tools.
    ann_data = pd.read_csv(os.path.join(
        dir_path_2, 'annuity_parameter.csv'), index_col='source')
    wd = ann_data.loc['epc_wind']
    epc_wind = economics.annuity(capex=wd['capex'], n=wd['n'], wacc=wd['wacc'])
    pvd = ann_data.loc['epc_pv']
    epc_pv = economics.annuity(
        capex=pvd['capex'], n=pvd['n'], wacc=pvd['wacc'])
    sd = ann_data.loc['epc_storage']
    epc_storage = economics.annuity(
        capex=sd['capex'], n=sd['n'], wacc=sd['wacc'])
    # create natural gas bus
    bgas = solph.Bus(label="natural_gas")

    # create electricity bus
    bel = solph.Bus(label="electricity")
    energysystem.add(bgas, bel)

    # create excess component for the electricity bus to allow overproduction
    excess = solph.Sink(label='excess_bel', inputs={bel: solph.Flow()})

    # create source object representing the natural gas commodity (annual limit)
    gas_resource = solph.Source(label='rgas',
                                outputs={bgas: solph.Flow(nominal_value=nominal_value_gas,
                                                          variable_costs=variable_cost_gas)})

    # create fixed source object representing wind power plants
    wind = solph.Source(label='wind', outputs={bel: solph.Flow(
        actual_value=data['wind'], fixed=True,
        investment=solph.Investment(ep_costs=epc_wind,
                                    maximum=max_cap_wind, existing=inst_wind_cap))})

    # create fixed source object representing pv power plants
    pv = solph.Source(label='pv', outputs={bel: solph.Flow(
        actual_value=data['pv'], fixed=True,
        investment=solph.Investment(ep_costs=epc_pv,
                                    maximum=max_cap_pv, existing=inst_pv_cap))})

    # create simple sink object representing the electrical demand
    demand = solph.Sink(label='demand', inputs={bel: solph.Flow(
        actual_value=data['demand_el'], fixed=True, nominal_value=1)})

    # create simple transformer object representing a gas power plant
    pp_gas = solph.Transformer(
        label="pp_gas",
        inputs={bgas: solph.Flow()},
        outputs={bel: solph.Flow(variable_costs=0)},
        conversion_factors={bel: 0.58})

    # create storage object representing a battery
    storage = solph.components.GenericStorage(
        label='storage',
        inputs={bel: solph.Flow()},
        outputs={bel: solph.Flow(variable_costs=0.0001)},
        loss_rate=0.00, initial_storage_level=None,
        invest_relation_input_capacity=1/6,
        invest_relation_output_capacity=1/6,
        inflow_conversion_factor=1, outflow_conversion_factor=0.8,
        investment=solph.Investment(ep_costs=epc_storage),
    )
    energysystem.add(excess, gas_resource, wind, pv, demand, pp_gas, storage)
    logging.info("Create energy system using oemof object.")
    return energysystem


# Optimise the energy system
def optimize(energysystem, data_path, fname='om_data'):
    """linear optimization of the energy system."""
    om = solph.Model(energysystem)
    om.solve(solver='cbc', solve_kwargs={'tee': False})
    # Dump results in disc for future analysis
    energysystem.results['main'] = outputlib.processing.results(om)
    energysystem.results['meta'] = outputlib.processing.meta_results(om)
    energysystem.dump(dpath=data_path, filename=fname)
    energysystem_data = energysystem
    logging.info("optimize wind, pv, gas_resource and storage.")
    return energysystem_data


def check_results_dataframe(energysystem_data):
    """Explore optimized supply, storage and investments. 
    Also calculates renewable share in the system.

    :dict: results
    :dataframe: elect_bus
    """
    # Restore dumped result for - later Processing *
    # energysystem = solph.EnergySystem()
    # energysystem.restore(
    #     dpath='../data/03_urban_energy_requirements/', filename='om_data')
    results = energysystem_data.results['main']
    electricity_bus = views.node(results, 'electricity')
    custom_storage = views.node(results, 'storage')
    elect_bus = electricity_bus['sequences']
    print('**electricity sequence head(5) **')
    print(elect_bus.head(5))
    storage_ = custom_storage['sequences']
    print('** Storage sequence head(5) **')
    print(storage_.head(5))
    my_results = electricity_bus['scalars']

    # installed capacity of storage in GWh
    my_results['storage_invest_GWh'] = (
        custom_storage['scalars'][(('storage', 'None'), 'invest')]/1e6)

    # installed capacity of wind power plant in MW
    my_results['wind_invest_MW'] = (
        electricity_bus['scalars'][(('wind', 'electricity'), 'invest')]/1e3)
    # resulting renewable energy share
    my_results['renewable_share'] = \
        (1 - electricity_bus['sequences'][(('pp_gas', 'electricity'), 'flow')].sum() /
         electricity_bus['sequences'][(('electricity', 'demand'), 'flow')].sum())
    logging.info("check optimisation results.")
    pp.pprint(my_results)


def plot(energysystem_data, year):
    """This code is copied from the oemof plotting examples.

    It allows for the customization of the plot using oemof/oev plotting object.
    See link here: `oemof-plotting_examples`_
    https://github.com/oemof/oemof-examples/tree/master/oemof_examples/oemof.solph/v0.3.x/plotting_examples
    """
    results = energysystem_data.results['main']
    cdict = {
        (('electricity', 'demand'), 'flow'): '#ce4aff',
        (('electricity', 'excess_bel'), 'flow'): '#555555',
        (('electricity', 'storage'), 'flow'): '#42c77a',
        (('pp_gas', 'electricity'), 'flow'): '#636f6b',
        (('pv', 'electricity'), 'flow'): '#ffde32',
        (('storage', 'electricity'), 'flow'): '#42c77a',
        (('wind', 'electricity'), 'flow'): '#5b5bae'}
    inorder = [(('pv', 'electricity'), 'flow'),
               (('wind', 'electricity'), 'flow'),
               (('storage', 'electricity'), 'flow'),
               (('pp_gas', 'electricity'), 'flow')]

    fig = plt.figure(figsize=(14, 8))
    electricity_seq = views.node(results, 'electricity')['sequences']
    plot_slice = oev.plot.slice_df(electricity_seq[str(year)+'-03-01':str(year)+'-03-10'],
                                   date_from=pd.datetime(year, 1, 1))
    my_plot = oev.plot.io_plot('electricity', plot_slice, cdict=cdict,
                               inorder=inorder, ax=fig.add_subplot(1, 1, 1),
                               smooth=True)
    ax = shape_legend('electricity', **my_plot)
    ax = oev.plot.set_datetime_ticks(ax, plot_slice.index, tick_distance=48,
                                     date_format='%d-%m-%H', offset=12)

    ax.set_ylabel('Power in MW')
    ax.set_xlabel(str(year))
    ax.set_title("Electricity bus")
    plt.savefig('../data/04_Visualisation/om.png', dpi=300)
    logging.info("Generate plot of optimized variables.")
    plt.show()


if __name__ == '__main__':

    dir_path_1 = '../data/03_urban_energy_requirements/'
    dir_path_2 = '../data/01_raw_input_data/'
    data = get_commodities(dir_path_1)
    year = data.index.year[10]
    max_cap_pv = round(get_installed_pv_capacity(dir_path_1)[1])  # KW
    max_cap_wind = get_installed_pv_capacity(dir_path_1)[0]  # KW

    # get economic values
    econs_values = pd.read_csv(os.path.join(
        dir_path_2, 'economic_data.csv'), index_col='economic_parameter')

    nominal_value_gas = econs_values.loc['nominal_value_gas[KW]']['values']
    variable_cost_gas = econs_values.loc['variable_cost_gas']['values']
    inst_wind_cap = econs_values.loc['inst_cap_wind[KW]']['values']
    inst_pv_cap = econs_values.loc['inst_cap_pv[KW]']['values']

    energysystem = oemof_power_system(data, dir_path_2, nominal_value_gas,
                                      variable_cost_gas, max_cap_pv,
                                      max_cap_wind, inst_pv_cap, inst_wind_cap)

    energysystem_data = optimize(energysystem, dir_path_1)
    check_results_dataframe(energysystem_data)
    plot(energysystem_data, year)
