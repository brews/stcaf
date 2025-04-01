from stcaf import build_sealevel_component_model_registry


def test_build_sealevel_component_model_registry():
    """
    Can we simply build_sealevel_component_model_registry(), populated, without error?
    """
    registry = build_sealevel_component_model_registry()
    # It should be populated with any keys or values.
    assert registry.keys()
    assert registry.values()


def test_plugin_registry_pkg_prefix():
    """
    Test that component models are registered with their parent package name as a prefix
    """
    registry = build_sealevel_component_model_registry()
    # 'bump' is an early registered test model in the stcaf package.
    assert "stcaf.bump" in registry
