# lSQEFS_supplementary
Supplementary materials for the paper "Structured Secant Methods to Select Smoothing Parameters For General Smooth Models"
by Krause, Borst, and van Rij (submitted).

## Replicating the simulations and results:
To run the simulations first make sure that you have R (>= 4.5) installed. The following packages
need to be installed:
  - mgcv
  - MSwM
  - gamair

Then set up a
[conda environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
with python > 3.10 and then run:

```
pip install "mssm[plot,mcmc]"
```

You also need to install the following python packages:
 - dotenv
 - rpy2

**Note:** ``rpy2`` is only required to replicate the Tweedie model example, since for that we need
``mgcv`` in R to compute the log-likelihood and derivatives. See
[here](https://rpy2.github.io/doc/latest/html/overview.html#install-installation) for install
instructions.

Finally, you will then need to set up an environment file at the top level of this repository called
``.env`` with the following variables:

```
n_cores=2 # Cores to use
conda_env=mssm13 # Name of conda environment to use
font_path=path/to/font/directory # Optionally a path to fonts (code wants to use Source Sans 3)
```

Then you can:
 - Clone this repository
 - run the ``run.sh`` script, which will automatically render all results

**Note**, ``run.sh`` will run all python/R scripts in parallel (the latter depend on the former).
Hence, if you want to make use of this script make sure to set ``n_cores`` to a low enough value.
