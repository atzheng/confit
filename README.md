# Features

- Manipulate configs (lists of dicts) in a lightweight, functional way. Includes vectorized functions from the excellent [[https://funcy.readthedocs.io/en/stable/index.html][funcy]] library, a dot notation mechanism for applying them in sequence.
- Automatically generate meaningful, human readable config ids.
- Easily summarise your configs and write them configs to separate directories.

# Example: Using Ficus in an ML Pipeline

A suggested pipeline for ML experiments:

1. Generate configs -- with Ficus!
2. Write scripts that integrate your configs, using e.g. [Sacred](https://github.com/IDSIA/sacred/blob/47ed504784d04b03cc30aaf15352b01711540cfa/docs/index.rst) or [Hydra](https://hydra.cc).
3. Run the scripts for each config -- workflow managers like [Snakemake](https://snakemake.readthedocs.io/en/stable/) or [Nextflow](https://www.nextflow.io) handle parallelization / dependencies beautifully.



