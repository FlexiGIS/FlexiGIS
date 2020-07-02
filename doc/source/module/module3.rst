.. module:: FlexiGIS

.. _module3:

Module III: Flexibisation optimisation
======================================
The spatial-temporal simulation outputs from Module I and II are time series of
electricity demand and supply. Theses generated datasets will be used by the `eomof-solph`_ model as
inputs to the linear optimisation problem. This module aims to determine the minimum system costs
at the given spatial urban scale while matching simultaneously the simulated electricity demand.
In addition, it aims to allocate and optimise distributed storage and other flexibility options
in urban energy systems. 

.. _Figure 5:
.. figure:: img/om.png

     Example result of optimal energy requirements, which minimize investement cost simulated for the city of Oldenburg.


.. _eomof-solph: https://oemof-solph.readthedocs.io/en/latest/index.html
