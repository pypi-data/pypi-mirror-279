from __future__ import annotations
import numpy

from est import settings
from est.io.information import InputInformation
from est.io.utils.read import get_data_from_url
from est.core.monotonic import split_piecewise_monotonic
from est.core.monotonic import piecewise_monotonic_interpolation_values


def read_bidirectional_spectra(
    information: InputInformation, timeout: float = settings.DEFAULT_READ_TIMEOUT
):
    """
    Method to read spectra acquired with the energy ramping up and down, with any number of repetitions.
    The read spectra is then interpolated to produce a 3D spectra (nb_energy_pts, nb_of_ramps, 1)

    Limitations:
      * The original spectra and energy datasets must 1D
    """
    raw_spectra = get_data_from_url(information.spectra_url, retry_timeout=timeout)
    raw_energy = get_data_from_url(information.channel_url, retry_timeout=timeout)
    config_url = information.config_url
    if config_url:
        config = get_data_from_url(config_url, retry_timeout=timeout)
    else:
        config = None

    ramp_slices = split_piecewise_monotonic(raw_energy)
    energy = piecewise_monotonic_interpolation_values(raw_energy, ramp_slices)

    interpolated_spectra = numpy.zeros(
        (len(energy), len(ramp_slices), 1), dtype=raw_spectra.dtype
    )
    for i, ramp_slice in enumerate(ramp_slices):
        interpolated_spectra[:, i, 0] = numpy.interp(
            energy,
            raw_energy[ramp_slice],
            raw_spectra[ramp_slice],
            left=numpy.nan,
            right=numpy.nan,
        )

    return interpolated_spectra, energy * information.energy_unit, config
