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

### Setup environment

The anaconda Python environment was used for analysis. The
`conda_env_settings.txt` file gives command line instructions for duplicating
the environment used, while a full list of packages is in `environment.yml`.

### Download data

Download the data files from
https://web.gin.g-node.org/willhart/sgn_costimulation. Set the variable
`BASE_PATH` in the `scripts/definitions.py` file to point to your data
directory. Do the same changes for `pulse_trains/scripts/definitions.py`. The
default is the `/Data` directory.

### Run analysis

The analysis can be run by executing `jupyter lab` in the terminal and opening
and running the `main` notebook. The first time the code is executed the
analysis will be saved to a pickled file. Subsequently the data can be rebuilt
by commenting out the relevant `%run` magic cells.

Pulse train data is included in a separate `pulse_trains` data within the code
directory. There is a fair bit of code duplication here but there are enough
differences to make integrating the two code-bases problematic.
