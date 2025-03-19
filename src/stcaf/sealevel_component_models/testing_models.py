"""
Various component models used for internal testing.
"""

from stcaf import Climate, SealevelComponent, SealevelComponentModel

import xarray as xr


class BumpModel(SealevelComponentModel):
    """
    Component model used for testing.
    """

    def __init__(self, bump: int | float = 1):
        self.bump = bump

    def preprocess(self, d: Climate) -> xr.Dataset:
        """
        Grabs 'temperature' variable from 'd' and adds bump to it.
        """
        ds = d.to_dataset()
        out = xr.Dataset({})
        out["temperature"] = ds["temperature"] + self.bump
        return out

    def fit(self, d: xr.Dataset) -> xr.Dataset:
        """
        Grabs 'temperature' variable from 'd' and adds bump to it.
        """
        out = xr.Dataset({})
        out["temperature"] = d["temperature"] + self.bump
        return out

    def project(self, d: xr.Dataset) -> xr.Dataset:
        """
        Grabs 'temperature' variable from 'd' and adds bump to it and returns it as a new 'sea_level_change' variable.
        """
        out = xr.Dataset({})
        out["sea_level_change"] = d["temperature"] + self.bump
        return out

    def postprocess(self, d: xr.Dataset) -> SealevelComponent:
        """
        Grabs 'sea_level_change' variable from 'd' and adds bump, returning it as a SealevelComponent.
        """
        out_ds = xr.Dataset({})
        out_ds["sea_level_change"] = d["sea_level_change"] + self.bump
        out = SealevelComponent(out_ds)
        return out
