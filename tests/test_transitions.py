from stcaf import (
    build_sealevel_component_model_registry,
    Climate,
    project_sealevel_components,
    integrate_sealevel_components,
    IntegratedSealevel,
    SealevelComponent,
)
from stcaf.sealevel_component_models.testing_models import BumpModel

import xarray as xr


def test_project_sealevel_components_single():
    """
    Test project_sealevel_components() give good output if we hand it a component model instance.
    """
    # Make up some input climate data
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

    # Build our expected output
    out_ds = xr.Dataset(
        {"sea_level_change": (["lat", "lon"], temperature)},
        coords={
            "lon": (["lon"], lon),
            "lat": (["lat"], lat),
        },
    )
    out_ds["sea_level_change"] += 4  # This is what we expect the component model to do.
    expected_component = SealevelComponent(out_ds)

    components = project_sealevel_components(climate, [BumpModel()])

    target_component = components[0]
    assert isinstance(target_component, SealevelComponent)
    assert len(components) == 1
    xr.testing.assert_allclose(
        target_component.to_dataset(), expected_component.to_dataset()
    )


def test_project_sealevel_components_registry_parameter():
    """
    Test project_sealevel_components() give good output if we hand it a model from registry, initialized with a parameter.
    """
    # Make up some input climate data
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

    # Build our expected output
    out_ds = xr.Dataset(
        {"sea_level_change": (["lat", "lon"], temperature)},
        coords={
            "lon": (["lon"], lon),
            "lat": (["lat"], lat),
        },
    )
    out_ds["sea_level_change"] += 8  # This is what we expect the component model to do.
    expected_component = SealevelComponent(out_ds)

    registry = build_sealevel_component_model_registry()

    components = project_sealevel_components(
        climate, [registry["testing_models.bump"](bump=2.0)]
    )

    target_component = components[0]
    assert isinstance(target_component, SealevelComponent)
    assert len(components) == 1
    xr.testing.assert_allclose(
        target_component.to_dataset(), expected_component.to_dataset()
    )


def test_integrate_sealevel_components():
    """
    Test that we can integrate two SealevelComponents.
    """
    # Make up two input sea level components
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

    # Integrated together we just expect them to be added into a 'sea_level_change' variable.
    isc_expected = IntegratedSealevel(in_ds1 + in_ds2)

    isc_actual = integrate_sealevel_components([slc1, slc2])

    assert isinstance(isc_actual, IntegratedSealevel)
    xr.testing.assert_allclose(isc_actual.to_dataset(), isc_expected.to_dataset())
