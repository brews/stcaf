# stcaf

[![codecov](https://codecov.io/gh/brews/stcaf/graph/badge.svg?token=6XFLZLFYDY)](https://codecov.io/gh/brews/stcaf)

Prototype framework for sea-level change modeling.

This is a prototype. It is likely to change in breaking ways. It might delete all your data so don't use it in production.

## Examples

This example reads in a NetCDF file with climate fields and applies models projecting components of sea level change, then integrates those components together.

```python

from stcaf import (
    build_sealevel_component_model_registry,
    Climate
    project_sealevel_components,
    integrate_sealevel_components,
)
import xarray as xr


climate = Climate(xr.open_dataset("example_climate_file.nc"))

# Collect sea level component models registered as plugins.
registry = build_sealevel_component_model_registry()

# Run registered models.
components = project_sealevel_components(
    climate,
    [
        registry["testing_models.bump"](),
        registry["testing_models.bump"](bump=2.0),
    ],
)

integrated_sealevel = integrate_sealevel_components(components)
```
The "bump" model is a toy used for testing. It takes input "temperature" and adds 1 to it for each model step: preprocess, fit, project, postprocess. The result is output as "sea_level_change". Setting the `bump` parameter when the model is intialized changes the size of each bump.

Component models can be any object following the `stcaf.SealevelComponentModel` protocol. You can pass these instances in directly or use them through the registry by registering the object at the "stcaf.sealevel_component_models" entrypoint of a Python package.

## Installation

Install the unreleased bleeding-edge version of the package with:
```
pip install git+https://github.com/brews/stcaf
```

## Support

Source code is available online at https://github.com/brews/stcaf/. This software is open source and available under the Apache License, Version 2.0.

Please file issues in the issue tracker at https://github.com/brews/stcaf/issues.
