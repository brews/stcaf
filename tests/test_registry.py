from stcaf import build_sealevel_component_model_registry


def test_build_sealevel_component_model_registry():
    """
    Can we simply build_sealevel_component_model_registry(), populated, without error?
    """
    registry = build_sealevel_component_model_registry()
    # It should be populated with any keys or values.
    assert registry.keys()
    assert registry.values()
