# Features

- Manipulate configs (lists of dicts) in a lightweight, functional way. Includes vectorized functions from the excellent [funcy](https://funcy.readthedocs.io/en/stable/index.html) library, a dot notation mechanism for applying them in sequence.
- automatically generate meaningful, human readable config ids.
- easily summarise your configs and write them configs to separate directories.

# example: using ficus in an ml pipeline

a suggested pipeline for ml experiments:

1. generate configs -- with ficus!
2. write scripts that integrate your configs, using e.g. [sacred](https://github.com/idsia/sacred/blob/47ed504784d04b03cc30aaf15352b01711540cfa/docs/index.rst) or [hydra](https://hydra.cc).
3. run the scripts for each config -- workflow managers like [snakemake](https://snakemake.readthedocs.io/en/stable/) or [nextflow](https://www.nextflow.io) handle parallelization / dependencies beautifully.



