import pytest
from typing import Sequence, List

import numpy
from est.core import monotonic


@pytest.mark.parametrize(
    "first_increasing", [True, False], ids=["first_increasing", "first_decreasing"]
)
@pytest.mark.parametrize(
    "clip_last_section", [True, False], ids=["clip_last", "no_clip"]
)
@pytest.mark.parametrize(
    "offset_fraction", [0, -0.1, 0.1], ids=["no_shift", "shift_down", "shift_up"]
)
@pytest.mark.parametrize("section_size", [3, 50])
@pytest.mark.parametrize("nsections", [1, 2, 3])
def test_split_piecewise_monotonic(
    first_increasing, clip_last_section, offset_fraction, section_size, nsections
):
    if clip_last_section and section_size <= 6:
        pytest.skip("no enough values to clip")

    if first_increasing:
        step = 1
    else:
        step = -1
    delta_value = 1.0
    offset = offset_fraction * delta_value
    do_offset = False

    values = list()
    indices = numpy.arange(section_size)

    expected_slices = list()
    expected_data = list()

    def _append(last):
        nonlocal values, step, do_offset

        data = indices * delta_value
        if do_offset:
            data = data + offset
        data = data[::step]
        if clip_last_section and last:
            data = data[: len(data) // 2]

        start = len(values)
        values.extend(data)
        stop = len(values)

        expected_slices.append(monotonic.create_slice(start, stop, step))
        if step == -1:
            expected_data.append(data[::-1])
        else:
            expected_data.append(data)

        step = -step
        do_offset = not do_offset

    for section_index in range(nsections):
        _append(section_index == (nsections - 1))

    slices = monotonic.split_piecewise_monotonic(values)

    try:
        assert len(slices) == nsections
        assert slices == expected_slices
        for slc, data in zip(slices, expected_data):
            numpy.testing.assert_array_equal(values[slc], data)
    except AssertionError:
        # Keep this for manual debugging
        # _plot_piecewise_monotonic(values, section_size, slices)
        raise


def _plot_piecewise_monotonic(
    values: Sequence[float], section_size: int, slices: List[slice]
):
    import matplotlib.pyplot as plt

    npoints = len(values)
    nsections = npoints // section_size + bool(npoints % section_size)
    for isection in range(nsections):
        start = isection * section_size
        stop = start + section_size
        y = values[start:stop]
        x = start + numpy.arange(len(y))
        plt.plot(x, y, "o-", color="green")

    x = [slc.start for slc in slices]
    y = [values[slc.start] for slc in slices]
    plt.plot(x, y, "o", color="red")
    plt.show()


def test_mean_nonzero():
    assert numpy.isnan(monotonic.mean_nonzero([]))
    assert monotonic.mean_nonzero([0]) == 0
    assert monotonic.mean_nonzero([0, 0, 1]) == 1
    assert monotonic.mean_nonzero([0, 0, 1, 2]) == 1.5


def test_first_monotonic_size():
    maxsize, avg_slope = monotonic.first_monotonic_size([])
    assert maxsize == 0
    assert numpy.isnan(avg_slope)

    maxsize, avg_slope = monotonic.first_monotonic_size([0])
    assert maxsize == 1
    assert numpy.isnan(avg_slope)

    maxsize, avg_slope = monotonic.first_monotonic_size([0, 0])
    assert maxsize == 2
    assert avg_slope == 0

    maxsize, avg_slope = monotonic.first_monotonic_size([1, 1])
    assert maxsize == 2
    assert avg_slope == 0

    maxsize, avg_slope = monotonic.first_monotonic_size([0, 1])
    assert maxsize == 2
    assert avg_slope == 1

    maxsize, avg_slope = monotonic.first_monotonic_size([0, 1, 0])
    assert maxsize == 2
    assert avg_slope == 1

    maxsize, avg_slope = monotonic.first_monotonic_size([0, -1])
    assert maxsize == 2
    assert avg_slope == -1

    maxsize, avg_slope = monotonic.first_monotonic_size([0, -1, 0])
    assert maxsize == 2
    assert avg_slope == -1

    maxsize, avg_slope = monotonic.first_monotonic_size([0, -1, -2, -2])
    assert maxsize == 4
    assert avg_slope == -1

    maxsize, avg_slope = monotonic.first_monotonic_size([0, -1, -2, -2, -1])
    assert maxsize == 4
    assert avg_slope == -1

    maxsize, avg_slope = monotonic.first_monotonic_size([0, 0, 1])
    assert maxsize == 3
    assert avg_slope == 1

    maxsize, avg_slope = monotonic.first_monotonic_size([0, 0, 1, 2, 1])
    assert maxsize == 4
    assert avg_slope == 1

    maxsize, avg_slope = monotonic.first_monotonic_size([0, 0, -1])
    assert maxsize == 3
    assert avg_slope == -1

    maxsize, avg_slope = monotonic.first_monotonic_size([0, 0, -1, -2, -1])
    assert maxsize == 4
    assert avg_slope == -1


def test_create_slice():
    values = numpy.arange(10)
    forward_slc = monotonic.create_slice(2, 5, 1)
    backward_slc = monotonic.create_slice(2, 5, -1)
    numpy.testing.assert_array_equal(values[forward_slc][::-1], values[backward_slc])

    forward_slc = monotonic.create_slice(2, len(values), 1)
    backward_slc = monotonic.create_slice(2, len(values), -1)
    numpy.testing.assert_array_equal(values[forward_slc][::-1], values[backward_slc])

    forward_slc = monotonic.create_slice(0, len(values) + 1, 1)
    backward_slc = monotonic.create_slice(0, len(values) + 1, -1)
    numpy.testing.assert_array_equal(values[forward_slc][::-1], values[backward_slc])
