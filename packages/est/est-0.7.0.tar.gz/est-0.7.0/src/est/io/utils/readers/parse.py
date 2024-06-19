import logging
from typing import Optional, Tuple

import numpy
from est.units import ur


_logger = logging.getLogger(__name__)


def parse_energy_mu(
    energy: Optional[numpy.ndarray],
    mu: Optional[numpy.ndarray],
    monitor: Optional[numpy.ndarray],
    energy_unit,
) -> Tuple[Optional[numpy.ndarray], Optional[numpy.ndarray]]:
    if energy is not None and mu is not None:
        if len(mu) != len(energy):
            raise ValueError(
                f"different number of elements between energy {len(energy)} and absorption {len(mu)}"
            )

    if energy is not None:
        energy = (energy * energy_unit).m_as(ur.eV)

    if mu is not None and monitor is not None:
        if len(mu) != len(monitor):
            raise ValueError(
                f"different number of elements between absorption {len(mu)} and monitor {len(monitor)}"
            )
        with numpy.errstate(divide="ignore"):
            mu = mu / monitor
        not_finite = ~numpy.isfinite(mu)
        if not_finite.any():
            _logger.warning(
                "found non-finite values after mu division by the monitor. Replace them by 0"
            )
            mu[not_finite] = 0

    return energy, mu
