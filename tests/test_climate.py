import xarray as xr
from stcaf import Climate


def test_climate_roundtrip():
    """
    Can we instantiate Climate from xarray.Dataset and get it back out?
    """
    # Making up some valid input data.
    lon = [-99.83, -99.32]
    lat = [42.25, 42.21]
    temperature = [[1, 2], [3, 4]]
    in_ds = xr.Dataset(
        {"temperature": (["lat", "lon"], temperature)},
        coords={
            "lon": (["lon"], lon),
            "lat": (["lat"], lat),
        },
    )

    climate = Climate(in_ds)
    out_ds = climate.to_dataset()

    xr.testing.assert_equal(in_ds, out_ds)
