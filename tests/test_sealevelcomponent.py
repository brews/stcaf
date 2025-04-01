import xarray as xr
from stcaf import SealevelComponent, filter_tag


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


def test_filter_tag():
    """
    Test that filter_tag filters the tag.

    Checks it works on components with or without .tags attr.
    """
    # Make up two input sea level components.
    # More involved than it needs to be.
    lon = [-99.83, -99.32]
    lat = [42.25, 42.21]
    slc = [[1.0, 2.0], [3.0, 4.0]]
    in_ds1 = xr.Dataset(
        {"sea_level_change": (["lat", "lon"], slc)},
        coords={
            "lon": (["lon"], lon),
            "lat": (["lat"], lat),
        },
    )
    slc1 = SealevelComponent(in_ds1)

    # Second input component is the first component + 1
    in_ds2 = in_ds1.copy(deep=True)
    in_ds2["sea_level_change"] += 1
    slc2 = SealevelComponent(in_ds2)

    # Third input component is the second component + 1
    in_ds3 = in_ds1.copy(deep=True)
    in_ds3["sea_level_change"] += 1
    slc3 = SealevelComponent(in_ds3)

    # Add tags to input.
    target_tag = "foo"  # This is the one we'll filter for.
    slc1.tags = set([target_tag, "bar"])
    slc2.tags = set()
    # slc3 has no tags attrs.
    components = [slc1, slc2, slc3]

    expected = [components[0]]

    actual = filter_tag(components, target_tag)

    assert actual == expected
