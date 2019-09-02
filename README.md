# Optogenetic costimulation

## About

This repository contains the scripts used for analysis of electrophysiology data
for the paper:

> *Combined Optogenetic and Electrical Stimulation of Auditory Neurons Increases
> Effective Stimulation Frequency* William L. Hart, Rachael T. Richardson,
> Tatiana Kameneva, Alex C. Thompson, Andrew K. Wise, James B. Fallon, Paul R.
> Stoddart, and Karina Needham

The source code can be found at
https://github.com/willhartneuro/sgn_costimulation and the data can be found at
https://web.gin.g-node.org/willhart/sgn_costimulation

## Running

The analysis can be run by executing `jupyter lab` in the terminal and opening
and running the `main` notebook. The first time the code is executed the
analysis will be saved to a pickled file. Subsequent executions can load from
the pickled file or can be re-run by setting `force_build_pickle = True`.
