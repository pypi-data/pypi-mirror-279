import numpy
import pytest

try:
    import larch
except ImportError:
    larch = None

from est.io.utils import ascii


def test_csv_reader(tmp_path):
    _test_read_spectrum(tmp_path, ".csv", "loopscan")


@pytest.mark.skipif(larch is None, reason="xraylarch not installed")
def test_larch_reader(tmp_path):
    _test_read_spectrum(tmp_path, ".xmu", "loopscan")


def test_spec_reader(tmp_path):
    _test_read_spectrum(tmp_path, ".spec", "loopscan")


def test_ascii_reader(tmp_path):
    _test_read_spectrum(tmp_path, ".dat", "loopscan")


def _test_read_spectrum(tmp_path, ext, scan_title):
    filename1 = str(tmp_path / f"data1{ext}")
    filename2 = str(tmp_path / f"data2{ext}")

    if ext == ".csv":
        delimiter = ","
    else:
        delimiter = " "

    if ext == ".csv":
        comments = ""
    else:
        comments = "#"

    energy_col_name = "energy"
    absorption_col_name = "mu"
    monitor_col_name = "monitor"

    if ext == ".spec":
        header1 = [
            f"F {str(filename1)}",
            "D Mon Jun 04 14:15:57 2012",
            "",
            f"S 1 {scan_title}",
            "D Mon Jun 04 14:15:57 2012",
            "N 2",
            f"L {energy_col_name}  {absorption_col_name}",
        ]
        header2 = [
            f"F {str(filename2)}",
            "D Mon Jun 04 14:15:57 2012",
            "",
            f"S 1 {scan_title}",
            "D Mon Jun 04 14:15:57 2012",
            "N 3",
            f"L {energy_col_name}  {absorption_col_name}  {monitor_col_name}",
        ]
        header1 = "\n".join(header1)
        header2 = "\n".join(header2)
        scan_title = f"1 {scan_title}"
    elif ext == ".dat":
        header1 = ""
        header2 = ""
        energy_col_name = "Column 1"
        absorption_col_name = "Column 2"
        monitor_col_name = "Column 3"
    else:
        header1 = delimiter.join(["energy", "mu"])
        header2 = delimiter.join(["energy", "mu", "monitor"])

    energy = numpy.arange(1, 11)
    mu = numpy.random.randint(low=1, high=100, size=10)
    monitor = numpy.random.randint(low=1, high=100, size=10)
    numpy.savetxt(
        filename1,
        numpy.array([energy, mu]).T,
        delimiter=delimiter,
        comments=comments,
        header=header1,
    )
    numpy.savetxt(
        filename2,
        numpy.array([energy, mu, monitor]).T,
        delimiter=delimiter,
        comments=comments,
        header=header2,
    )

    renergy, rmu = ascii.read_spectrum(
        filename1,
        energy_col_name=energy_col_name,
        absorption_col_name=absorption_col_name,
        monitor_col_name=monitor_col_name,
        scan_title=scan_title,
    )
    numpy.testing.assert_array_equal(energy, renergy)
    numpy.testing.assert_array_equal(mu, rmu)

    renergy, rmu = ascii.read_spectrum(
        filename2,
        energy_col_name=energy_col_name,
        absorption_col_name=absorption_col_name,
        monitor_col_name=monitor_col_name,
        scan_title=scan_title,
    )
    numpy.testing.assert_array_equal(energy, renergy)
    numpy.testing.assert_array_equal(mu / monitor, rmu)
