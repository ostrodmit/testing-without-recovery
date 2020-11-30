# Near-Optimal Model Discrimination with Non-Disclosure

Matlab implementation of numerical experiments from the paper

[Dmitrii M. Ostrovskii, Mohamed Ndaoud, Adel Javanmard, Meisam Razaviyayn. Near-Optimal Model Discrimination with Non-Disclosure Property](https://arxiv.org/abs/1810.06838)

To run the experiments, clone or download the repository and run 
```
run_all.py
```
The data for the curves will appear in ``data/gauss``

The experiments that reproduce the curves reported in the paper take a few days to run. To obtain (less accurate) results faster,
change the number of Monte-Carlo trials: parameter ``T`` in ``run_all.py``. 
