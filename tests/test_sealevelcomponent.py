import xarray as xr
from stcaf import SealevelComponent


def test_sealevelcomponent_roundtrip():
    """
    Can we instantiate SealevelComponent from xarray.Dataset and get it back out?
    """
    # Making up some valid input data.
    lon = [-99.83, -99.32]
    lat = [42.25, 42.21]
    slc = [[1, 2], [3, 4]]
    in_ds = xr.Dataset(
        {"sea_level_change": (["lat", "lon"], slc)},
        coords={
            "lon": (["lon"], lon),
            "lat": (["lat"], lat),
        },
    )

    sealevelcomponent = SealevelComponent(in_ds)
    out_ds = sealevelcomponent.to_dataset()

    xr.testing.assert_equal(in_ds, out_ds)
