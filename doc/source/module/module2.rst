.. module:: FlexiGISdoc

.. _module2:

Module II: Modelling urban energy requirements
===============================================
This module simulates urban energy requirements (consumption and generation). The spatio-temporal
electricity consumption and renewable energy generation from PV and wind, in the defined
urban area are modeled. This component models the combined spatial parameters of urban
geometries (Module I) and links them to real-world applications using GIS. Here, a
bottom-up simulation approach is developed to calculate local urban electricity demand
and power generation from available renewable energy resources. For instance, using open
source datasets like Standardised Load Profiles and publicly available weather data.
`Figure 4`_ shows the generated quarter-hourly time series of the aggregated load and PV power
supply profile for investigated case study.

.. _Figure 4:
.. figure:: img/Energy_Re.png

    Simulated electricity consumption (green) and solar power generation (red) for the city of Oldenburg.
