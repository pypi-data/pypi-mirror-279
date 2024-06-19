import logging
import functools
from typing import Tuple, List, Optional

import numpy

from .abstract_ascii import AbstractAsciiReader
from est.units import ur
from .parse import parse_energy_mu

_logger = logging.getLogger(__name__)


def _ascii_header(ascii_file: str) -> Tuple[List[str], str, int]:
    firstline = ""
    skiprows = 0
    with open(ascii_file, "r") as csvfile:
        while not firstline or firstline.startswith("#"):
            firstline = csvfile.readline().strip()
            skiprows += 1

    for delimiter in [",", ";", " "]:
        columns = firstline.split(delimiter)
        if len(columns) > 1:
            break

    try:
        float(columns[0])
    except ValueError:
        columns = [s.strip() for s in columns]
        return columns, delimiter, skiprows
    skiprows -= 1
    columns = [f"Column {i+1}" for i in range(len(columns))]
    return columns, delimiter, skiprows


class AsciiReader(AbstractAsciiReader):
    @staticmethod
    def get_scan_column_names(file_path: str, scan_title: str) -> List[str]:
        columns, _, _ = _ascii_header(file_path)
        return columns

    @staticmethod
    @functools.lru_cache(maxsize=2)  # called twice for energy and absorption
    def read_spectrum(
        ascii_file,
        energy_col_name=None,
        absorption_col_name=None,
        monitor_col_name=None,
        energy_unit=ur.eV,
        scan_title=None,
    ) -> Tuple[Optional[numpy.ndarray], Optional[numpy.ndarray]]:
        columns, delimiter, skiprows = _ascii_header(ascii_file)
        if not columns:
            return None, None
        if energy_col_name is None:
            _logger.warning(
                "Spec energy column name not provided. Select the first column."
            )
            energy_col_name = columns[0]
        if absorption_col_name is None:
            _logger.warning(
                "Spec absorption column name not provided. Select the second column."
            )
            if len(columns) > 1:
                absorption_col_name = columns[1]

        has_energy = energy_col_name in columns
        has_absorption = absorption_col_name in columns
        if not has_energy and not has_absorption:
            return None, None

        has_monitor = monitor_col_name in columns
        usecols = list()
        names = list()
        if has_energy:
            usecols.append(columns.index(energy_col_name))
            names.append("energy")
        if has_absorption:
            usecols.append(columns.index(absorption_col_name))
            names.append("mu")
        if has_monitor:
            usecols.append(columns.index(monitor_col_name))
            names.append("monitor")

        data = numpy.loadtxt(
            ascii_file, delimiter=delimiter, skiprows=skiprows, usecols=usecols
        )
        data = dict(zip(names, data.T))
        energy = data.get("energy")
        mu = data.get("mu")
        monitor = data.get("monitor")

        return parse_energy_mu(energy, mu, monitor, energy_unit)
