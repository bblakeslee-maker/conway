# John Conway's Game of Life

A small implementation of the Game of Life.

## Installation

Dependencies can be installed with:
```bash
conda env create -f environment.yml
```

## Invocation

A simulation can be started with:
```bash
python3 main.py --config path/to/config.yaml
```

## Supported Configuration Parameters

 * `height`: Height of simulation world.
 * `interval`: Seconds between each world update.
 * `iterations`: Number of iterations to run for.
 * `threshold`: Value between `0.0` and `1.0` for generating a live cell.
 * `width`: Width of simulation world.
 * `world`: Hardcoded world to start from.  See `configs/default_fixed.yaml` for details.