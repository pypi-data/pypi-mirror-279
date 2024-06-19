import akida
from enum import Enum

from .core import LayerType


class MapMode(Enum):
    """ Mapping mode

    Define the strategy for the hardware mapping.
    """
    AllNps = 1
    """ Maximize HW ressources (number of NPs used) with minimum HW passes."""
    HwPr = 2
    """ Maximize HW ressources (number of NPs used) with maximum HW passes.
    This mode provides the potential for higher-performances"""
    Minimal = 3
    """ Minimize HW ressources or mode to use a custom MeshMapper"""


class SplitByValues(akida.MeshMapper):
    """ A custom MeshMapper that splits layers

    Args:
        split_width (int, optional): the split on width. Defaults to 64.
        split_height (int): the split on height. Defaults to 256.
        split_neurons (int): the split on filters. Defaults to 512.
    """
    def __init__(self, split_width=64, split_height=256, split_neurons=512):
        akida.MeshMapper.__init__(self)
        self.split_width = split_width
        self.split_height = split_height
        self.split_neurons = split_neurons

    def select_nps(self, source_nps, num_nps, type):
        return source_nps[:num_nps]

    def cnp_max_width(self):
        return self.split_width

    def cnp_max_height(self):
        return self.split_height

    def cnp_max_filters(self):
        return self.split_neurons


def _get_layer_mapped(model):
    return sum(1 for layer in model.layers if layer.mapping is not None)


def _get_model_pass(model):
    nb_pass = 0
    for seq in model.sequences:
        nb_pass += len(seq.passes)
    return nb_pass


def _get_model_seq(model):
    return len(model.sequences)


def _get_model_nps(model):
    hrc_layers = [LayerType.InputConvolutional, LayerType.InputConv2D, LayerType.Stem]

    nb_nps = 0
    for seq in model.sequences:
        for current_pass in seq.passes:
            for layer in current_pass.layers:
                # The layer is mapped on NPs but not on HRC
                if layer.parameters.layer_type not in hrc_layers and layer.mapping is not None:
                    nb_nps += len(layer.mapping.nps)

    return nb_nps


def _map_splited_model(model, device, hw_only, neurons):
    try:
        split_width = 32 if device.version.product_id in [0, 0xa1] else 64
        mapper = SplitByValues(split_neurons=neurons, split_width=split_width)
        akida.MeshMapper.replace(mapper)
        model._map(device, hw_only=hw_only)
    finally:
        # TODO restore the previous mesh mapper
        akida.MeshMapper.replace(None)
    return model


def _is_better_map(model_ref, model_cur, consider_pass_nb=True):
    # Returns if a current model has a better mapping than a reference model
    nb_layer_mapped_ref = _get_layer_mapped(model_ref)
    nb_layer_mapped_cur = _get_layer_mapped(model_cur)

    # Better if more layers mapped
    if nb_layer_mapped_ref != nb_layer_mapped_cur:
        return nb_layer_mapped_ref < nb_layer_mapped_cur

    nb_seq_ref = _get_model_seq(model_ref)
    nb_seq_cur = _get_model_seq(model_cur)

    # Better with low seq number
    if nb_seq_ref != nb_seq_cur:
        return nb_seq_cur < nb_seq_ref

    if consider_pass_nb:
        np_pass_ref = _get_model_pass(model_ref)
        np_pass_cur = _get_model_pass(model_cur)
        if np_pass_ref != np_pass_cur:
            # Better if less passes
            return np_pass_cur < np_pass_ref

    nb_nps_ref = _get_model_nps(model_ref)
    nb_nps_cur = _get_model_nps(model_cur)
    # Better if we use more NPs
    return nb_nps_ref <= nb_nps_cur


def _map_search(model, device, hw_only, min_pass):
    # Obtains the reference mapped model, using the minimal hardware ressources
    try:
        model_ref = akida.Model(layers=model.layers[:])
    except Exception:
        # If cannot copy the model, we use Minimal mapping
        model._map(device, hw_only=hw_only)
        return

    model_ref._map(device, hw_only=hw_only)

    # TODO retrieved the defaults split values
    min_split_neurons = 0
    max_split_neurons = 512
    cur_split_neurons = max_split_neurons
    best_split_neurons = -1

    while min_split_neurons + 2 <= max_split_neurons:
        cur_split_neurons = int((min_split_neurons + max_split_neurons) / 2)
        assert cur_split_neurons > 0
        try:
            model_cur = akida.Model(layers=model.layers[:])
            model_cur = _map_splited_model(model_cur, device, hw_only=hw_only,
                                           neurons=cur_split_neurons)
            if _is_better_map(model_ref, model_cur, min_pass):
                model_ref = model_cur
                max_split_neurons = cur_split_neurons
                best_split_neurons = cur_split_neurons
            else:
                min_split_neurons = cur_split_neurons
            del model_cur
        except Exception:
            min_split_neurons = cur_split_neurons

    # Apply mapping to model
    if best_split_neurons > 0:
        # Apply mapping found
        _map_splited_model(model, device, hw_only=hw_only, neurons=best_split_neurons)
    else:
        # Apply default mapping because not better was found
        model._map(device, hw_only=hw_only)
