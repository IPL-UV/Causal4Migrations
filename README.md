# Causal4Migrations
This repo contains data, demos and code snippets to reproduce the results of our work on causal discovery of drought-induced human displacement drivers.

# Abstract

Human displacement is often linked to climate change not without reason: the increasing frequency, intensity, and duration of droughts are expected to impact the livelihoods of millions. However, lacking knowledge about human mobility in drought contexts restricts effective modelling and forecasting. Drought displacement is multicausal and contextual, and its key drivers, associated timescales, and causal-effect lags are uncertain and often assessed using mechanistic models and qualitative assumptions. Here, we propose a quantitative data-driven approach to model and discover the causes of drought-induced displacement in Somalia over the period 2010-2022. Our approach recognizes the context-specific causality of different districts and highlights specific vulnerabilities associated with water and food security systems and violent conflict episodes. Our results pave the way towards algorithms capable of discovering knowledge from human mobility data for anticipation, policy-making, and humanitarian aid.

# Results

![image](Motivational_Figure_IDP_Somalia.pdf)
Pipeline overview to understand internal displacement through causal discovery. Total number and percentage of new displacements attributed to droughts and conflicts in Somalia during the years 2010-2022 (a). The three selected Somalia districts included in the study (Baidoa, Diinsoor, Qoryooley) are analyzed between $2010-2022$ with environmental (precipitation), socioeconomic (food, livestock, and water prices), and conflict drivers (fatalities) (b). Preprocessing of the time series and the application of conditional independence tests, we derive causal graphs per district with the PCMCI method (c).

# Data and code availability

All the analysis was performed in python.

# How to cite our work

If you find this useful, consider citing our work:

><b>Causal discovery of drought-induced human displacement drivers</b>
José María Tárraga, Gustau Camps-Valls, Maria Piles, Eva Sevillano-Marco, Michele Ronco, María Teresa Miranda, Qiang Wang, Jordi Cerdà and Jordi Muñoz, 
Science Advances, 2023

```
@article {Tarraga2022,
  author = {Tárraga, J.M and Camps-Valls, G. and Piles, M. and Sevillano-Marco, E. and Ronco, M. and Miranda, M.T. and Wang, Q. and Cerdà, J. and Muñoz, J.},
  title = {Causal discovery of drought-induced human displacement drivers},
  volume = {},
  number = {},
  year = {2023},
  doi = {},
  publisher = {},
  URL = {},
  journal = {}
}
```

# Acknowledgements
The authors thank IDMC, Ivana Hajzmanova and Sylvain Ponsere for facilitating access to data and humanitarian actors in the country. the authors want to thank Albert Abou and Tessa Richardson from the IDP Working Group for the IDP data provided. Rogerio Bonifacio, Oscar Caccavale, Joseph Hooker and Giancarlo Pini from the World Food Programme for their useful comments provided on market prices. The authors also thank Abdoulaye Diallo and Abdulkadir Gure from the WASH cluster Somalia and Paolo Paron from FAO SWALIM for their insights and reporting about the water availability situation in Somalia.
This work has received funding from the European Union's Horizon 2020 Research and Innovation Project 'DeepCube: Explainable AI pipelines for big Copernicus data' (grant agreement No 101004188). GCV would like to acknowledge the support from the European Research Council (ERC) under the ERC Synergy Grant USMILE (grant agreement 855187), and the Fundación BBVA with the project 'Causal inference in the human-biosphere coupled system (SCALE)'. 
