.. module:: FlexiGIS

.. _flexigis_optimize.py:

flexigis_optimize.py
======================
.. automodule:: flexigis_optimize
    :members:


This script is use to model an energy system, and derive the optimal RE feedin capacity and
storage investment. The optimisation is carried out using
the oemof solph package. The below codes are taken from the `oemof-example`_ codes 
github repository. The optimization settings are described below by the
following parameters:

- optimize wind, pv, gas_resource and storage
- set investment cost for wind, pv and storage
- set gas price for kWh


See links: `oemof-example`_ and `oemof-plotting_examples`_

.. _oemof-example: https://github.com/oemof/oemof-examples/blob/master/oemof_examples/oemof.solph/v0.3.x/storage_investment/v1_invest_optimize_all_technologies.py
.. _oemof-plotting_examples: https://github.com/oemof/oemof-examples/tree/master/oemof_examples/oemof.solph/v0.3.x/plotting_examples.