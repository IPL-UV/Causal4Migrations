# Causal4Migrations

# Abstract

The increasing frequency and severity of droughts present a significant risk to vulnerable regions of the globe, potentially leading to substantial human displacement in extreme situations. Drought-induced displacement is a complex and multifaceted issue that can perpetuate cycles of poverty, exacerbate food and water scarcity, and reinforce socio-economic inequalities. However, our understanding of human mobility in drought scenarios is currently limited, inhibiting accurate predictions and effective policy responses. Drought-induced displacement is driven by numerous factors and identifying its key drivers, causal-effect lags, and consequential effects is often challenging, typically relying on mechanistic models and qualitative assumptions. This paper presents a novel, data-driven methodology, grounded in causal discovery, to retrieve the drivers of drought-induced displacement within Somalia from 2016 to 2023. Our model exposes the intertwined vulnerabilities and the leading times that connect drought impacts, water and food security systems along with episodes of violent conflict, emphasizing the context-specific causality across various districts. These findings pave the way for the development of algorithms with the ability to learn from human mobility data, enhancing anticipatory action, policy formulation, and humanitarian aid.

# Results
![Motivational_Figure](https://github.com/IPL-UV/Causal4Migrations/assets/86777598/4220b3ca-a00a-4a22-b483-afdb784a0b1b)

Pipeline overview to understand internal displacement through causal discovery. Total number and percentage of new displacements attributed to droughts and conflicts in Somalia during the years 2016-2023 (a). The three selected Somalia districts included in the study (Baidoa, Diinsoor, Kurtunwarey) are analyzed between $2016-2023$ with weather (SPEI), socioeconomic (food, livestock, and water prices), and conflict drivers (fatalities) (b). Preprocessing of the time series and the application of conditional independence tests, we derive causal graphs per district with the PCMCI method (c).

# Data and code availability

All the analysis was performed in python, data and code are fully available under this repository.

# How to cite our work

If you find this useful, consider citing our work:

><b>Causal discovery reveals complex patterns of drought-induced displacement</b>
José María Tárraga,  Eva Sevillano-Marco, Jordi Muñoz, Maria Piles, Vasileios Sitokonstantinou, Michele Ronco, María Teresa Miranda, Jordi Cerdà and Gustau Camps-Valls, 2023

```
@article {Tarraga2024,
  author = {Tárraga, J.M and Sevillano-Marco, E. and Muñoz, J. and Piles, M. and Sitokonstantinou, V. and Ronco, M. and Miranda, M.T. and Cerdà, J. and Camps-Valls, G.},
  title = {Causal discovery reveals complex patterns of drought-induced displacement},
  volume = {},
  number = {},
  year = {2024},
  doi = {},
  publisher = {},
  URL = {},
  journal = {}
}
```

# Acknowledgements
The authors thank IDMC, Ivana Hajzmanova, and Sylvain Ponsere for facilitating access to data and humanitarian actors in the country. The authors want to thank Albert Abou and Tessa Richardson from the IDP Working Group for the IDP data provided. Rogerio Bonifacio, Oscar Caccavale, Joseph Hooker, and Giancarlo Pini from the World Food Programme for their helpful comments on market price preprocessing. The authors also thank Abdoulaye Diallo and Abdulkadir Gure from the WASH cluster Somalia and Paolo Paron from FAO SWALIM for their insights and reporting about the water availability situation and data collection in Somalia. 
This work has received funding from the European Union's Horizon 2020 Research and Innovation Project 'DeepCube: Explainable AI pipelines for big Copernicus data' (grant agreement No 101004188). GCV would like to acknowledge the support from the European Research Council (ERC) under the ERC Synergy Grant USMILE (grant agreement 855187), and the Fundación BBVA with the project 'Causal inference in the human-biosphere coupled system (SCALE)'. 
