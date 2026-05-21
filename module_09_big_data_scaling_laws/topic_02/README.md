# Module 09 — Topic 02: Scaling Laws in Natural Hazards

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Digihaz/digihaz-course-materials/blob/main/module_09_big_data_scaling_laws/topic_02/notebooks/02_exercise.ipynb)

## Learning Objectives

By the end of this topic students will be able to:

1. Objective 1: Understanding the information inside the seismic catalogues.
2. Objective 2: Preparation of catalogues for research purposes.
3. Objective 3: Perform the declustering of the catalogue.
4. Objective 4: Understanding the meaning of the Gutenberg-Richter Law.
5. Objective 5: Computing the seismic parameters of the catalogue.
6. Objective 6: Evaluating the influence of the declustering on the results.

## Contents

| File | Description |
|------|-------------|
| `notebooks/01_lecture.ipynb`  | Lecture Seismic Catalogue preparation (I) |
| `notebooks/02_exercise.ipynb` | Student exercise for lecture 1 |
| `notebooks/03_lecture.ipynb`  | Lecture Seismic Catalogue preparation (II) |
| `notebooks/04_exercise.ipynb` | Student exercise for lecture 2 |
| `slides/` | PDF slide exports |
| `data/` | Sample datasets |
| `arduino/` | Embedded hardware sketches |

## References

- [Storchak, D.A., D. Di Giacomo, I. Bondár, E.R. Engdahl, J. Harris, W.H.K. Lee, A. Villaseñor and P. Bormann (2013). Public Release of the ISC-GEM Global Instrumental Earthquake Catalogue (1900-2009). Seism. Res. Lett., 84, 5, 810-815, doi: 10.1785/0220130034]
- [Storchak, D.A., D. Di Giacomo, E.R. Engdahl, J. Harris, I. Bondár, W.H.K. Lee, P. Bormann and A. Villaseñor (2015). The ISC-GEM Global Instrumental Earthquake Catalogue (1900-2009): Introduction, Phys. Earth Planet. Int., 239, 48-63, doi: 10.1016/j.pepi.2014.06.009]
- [Di Giacomo, D., E.R. Engdahl and D.A. Storchak (2018). The ISC-GEM Earthquake Catalogue (1904–2014): status after the Extension Project, Earth Syst. Sci. Data, 10, 1877-1899, doi: 10.5194/essd-10-1877-2018.]
- [IGN-UPM Working Group (2013). Actualización de mapas de peligrosidad sísmica de España 2012 (in Spanish), Centro Nacional de Información Geográfica,325 pp., https://www.ign.es/resources/acercaDe/libDigPub/ActualizacionMapasPeligrosidadSismica2012.pdf]
- [Omori, F. (1894). On the Aftershocks of Earthquakes, Journal of the College of Science, Imperial University of Tokyo.]
- [Utsu, T. (1961). A statistical study on the occurrence of aftershocks, Geophysical Magazine, 30, 521–605.]
- [M. Pagani, D. Monelli, G. Weatherill, L. Danciu, H. Crowley, V. Silva, P. Henshaw, L. Butler, M. Nastasi, L. Panzeri, M. Simionato, D. Vigano (2014). OpenQuake Engine: An Open Hazard (and Risk) Software for the Global Earthquake Model. Seismological Research Letters, 85 (3): 692–702. doi: https://doi.org/10.1785/0220130087]
- [Gardner, J. K. and Knopoff, L. (1974). Is the sequence of earthquakes in Southern California, with aftershocks removed, Poissonian?, Bulletin of the Seismological Society of America, 64, 1363–1367, https://doi.org/10.1785/BSSA0640051363.]
- [Reasenberg, P. A. (1985). Second-order moment of central California seismicity, 1969–1982, Journal of Geophysical Research: Solid Earth, 90, 5479–5495, https://doi.org/10.1029/JB090iB07p05479.]
- [Reasenberg, P. A. and Jones, L. M. (1989). Earthquake Hazard After a Mainshock in California, Science, 243, 1173–1176, https://doi.org/10.1126/science.243.4895.1173.]
- [Uhrhammer, R. A. (1986). Characteristics of northern and southern California seismicity, Earthquake Notes, 57, 21–37.]
- [Zaliapin, I., Gabrielov, A., Keilis-Borok, V., and Wong, H. (2008). Clustering Analysis of Seismicity and Aftershock Identification, Physical Review Letters, 101, 018 501, https://doi.org/10.1103/PhysRevLett.101.018501]
- [Zaliapin, I. and Ben-Zion, Y. (2013a). Earthquake clusters in southern California I: Identification and stability, Journal of Geophysical Research: Solid Earth, 118, 2847–2864, https://doi.org/10.1002/jgrb.50179]
- [Zaliapin, I. and Ben-Zion, Y. (2013b). Earthquake clusters in southern California II: Classification and relation to physical properties of the crust, Journal of Geophysical Research: Solid Earth, 118, 2865–2877, https://doi.org/10.1002/jgrb.50178 ]
- [Zaliapin, I. and Ben-Zion, Y. (2016). A global classification and characterization of earthquake clusters, Geophysical Journal International, 207, 608–634, https://doi.org/10.1093/gji/ggw300]
- [Zaliapin, I. and Ben-Zion, Y. (2020). Earthquake Declustering Using the Nearest-Neighbor Approach in Space-Time-Magnitude Domain, Journal of Geophysical Research: Solid Earth, 125, e2018JB017, https://doi.org/10.1029/2018JB017120 ]
- [Ogata, Y. (1988). Statistical Models for Earthquake Occurrences and Residual Analysis for Point Processes, Journal of the American Statistical Association, 83, 9–27, https://doi.org/10.2307/2288914]
- [Ogata, Y. (1998). Space-Time Point-Process Models for Earthquake Occurrences, Annals of the Institute of Statistical Mathematics, 50, 379–402, https://doi.org/10.1023/A:1003403601725]
- [Gutenberg, B. and Richter, C. F. (1944). Frequency of earthquakes in California, Bulletin of the Seismological Society of America, 34, 185–188.]
- [Gulia, L., Tormann, T., Wiemer, S., Herrmann, M., and Seif, S. (2016). Short-term probabilistic earthquake risk assessment considering time-dependent b values, Geophysical Research Letters, 43, 1100–1108, https://doi.org/10.1002/2015GL066686.]
- [Aki, K. (1965). Maximum likelihood estimate of b in the formula log N= a-bM and its confidence limits, Bulletin of the Earthquake Research Insitute, Tokyo University, 43, 237–239.]
- [Utsu, T. (1966). A statistical significance test of the difference in b-value between two earthquake groups, Journal of Physics of the Earth, 14, 37–40, https://doi.org/10.4294/jpe1952.14.37.]
- [Bath, M. (1965). Lateral inhomogeneities of the upper mantle, Tectonophysics, 2, 483–514, https://doi.org/10.1016/0040-1951(65)90003-X.]
