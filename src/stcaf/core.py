from abc import abstractmethod
from importlib.metadata import entry_points
from typing import Protocol, runtime_checkable, Sequence

import xarray as xr


def read_climate(uri_or_buffer) -> "Climate":
    return Climate(xr.open_dataset(uri_or_buffer))


class Climate:
    """
    Climate fields input for sea level modeling
    """

    def __init__(self, d: xr.Dataset):
        self._d = d

    def to_dataset(self) -> xr.Dataset:
        return self._d.copy()


# TODO: should this be a SealevelChangeComponent or a SealevelComponent. Do we care about that distinction?
# TODO: Could this hold a DataArray rather than a Dataset? Need multiple variables.
class SealevelComponent:
    """
    Component of projected sea level
    """

    def __init__(self, d: xr.Dataset):
        # Quickly check some invariants.
        # TODO: Other invariants?
        # TODO: Unsure if "lat", "lon" should be coord or data variables.
        if "sea_level_change" not in d.data_vars:
            raise ValueError("sea_level_change is not a data variable in the input")
        if "lat" not in d.variables:
            raise ValueError("lat is not a variable in the input")
        if "lon" not in d.variables:
            raise ValueError("lon is not a variable in the input")

        self._d = d  # Maybe just expose this as a property, test invariants then?

    def to_dataset(self) -> xr.Dataset:
        return self._d.copy()


# TODO: Should this be a separate class or not? How important is the sequence of steps?
class IntegratedSealevel:
    """
    Projected sea-level from integrated components
    """

    def __init__(self, d: xr.Dataset):
        # Quickly check some invariants.
        # TODO: Unsure if "lat", "lon" should be coord or data variables.
        if "sea_level_change" not in d.data_vars:
            raise ValueError("sea_level_change is not a data variable in the input")
        if "lat" not in d.variables:
            raise ValueError("lat is not a data variable in the input")
        if "lon" not in d.variables:
            raise ValueError("lon is not a data variable in the input")

        self._d = d  # Maybe just expose this as a property, test invariants then?

    def to_dataset(self) -> xr.Dataset:
        return self._d.copy()


class ExtremeSealevel: ...


def project_sealevel_components(
    d: Climate, models: Sequence["SealevelComponentModel"]
) -> Sequence[SealevelComponent]:
    """
    Use models to project sealevel components.
    """
    out = []
    for model in models:
        # Storing sequence outputs like this can take more memory, but makes it easier for users to debug issues in this sequence.
        preprocessed = model.preprocess(d)
        fitted = model.fit(preprocessed)  # Is this fed back in for projecting?!?
        projected = model.project(fitted)
        postprocessed = model.postprocess(projected)
        out.append(postprocessed)

    return out


def filter_tag(
    components: Sequence[SealevelComponent], tag=str
) -> Sequence[SealevelComponent]:
    """
    Return only components, c, with "tag" in `c.tags`.
    """
    return [c for c in components if tag in getattr(c, "tags", set())]


def integrate_sealevel_components(
    components: Sequence[SealevelComponent],
) -> IntegratedSealevel:
    """
    Create integrated sealevel from components by summing components together.
    """
    # Tries combining components along common dimensions and a new, temporary "component" dim.
    # Then sums "sea_level_change" of all components into one, removing the temporary "component" dim.
    component_dim = "component"
    single_ds = xr.concat((c.to_dataset() for c in components), dim=component_dim)
    total_out = single_ds[["sea_level_change"]].sum(dim=component_dim)
    return IntegratedSealevel(total_out)


# Not confident this sequence is representative of the model progression. Not intuitive?
@runtime_checkable
class SealevelComponentModel(Protocol):
    @abstractmethod
    def preprocess(self, d: Climate) -> xr.Dataset:
        raise NotImplementedError

    @abstractmethod
    def fit(self, d: xr.Dataset) -> xr.Dataset:
        raise NotImplementedError

    @abstractmethod
    def project(self, d: xr.Dataset) -> xr.Dataset:
        raise NotImplementedError

    @abstractmethod
    def postprocess(self, d: xr.Dataset) -> SealevelComponent:
        raise NotImplementedError


def build_sealevel_component_model_registry() -> dict[str, SealevelComponentModel]:
    """
    Build a dictionary with {key: component_model_class} from package plugins.
    """
    registry = {}

    # Load plugins from package entrypoint
    discovered_plugins = entry_points(group="stcaf.sealevel_component_models")
    for plugin in discovered_plugins:
        # TODO: Logging debug might be good here.
        # TODO: Emit warning on conflicts or if key overwritten.
        # Some kind of check against the protocol? etc?

        # Register plugins under their parent package name, if available.
        entry_key = str(plugin.name)
        if plugin.dist is not None:
            entry_key = f"{plugin.dist.name}.{plugin.name}"

        registry[entry_key] = plugin.load()

    return registry
