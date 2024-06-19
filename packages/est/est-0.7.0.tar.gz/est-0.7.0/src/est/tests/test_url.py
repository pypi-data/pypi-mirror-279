from est.io.utils.ascii import build_ascii_data_url, split_ascii_url
from silx.io.url import DataUrl


def test_spec_url():
    """simple test of the spec url function class"""
    file_path = "test.dat"
    scan_title = "1.1"
    col_name = "energy"
    data_slice = None
    url = build_ascii_data_url(
        file_path=file_path,
        scan_title=scan_title,
        col_name=col_name,
        data_slice=data_slice,
    )
    assert isinstance(url, DataUrl)
    assert split_ascii_url(url) == {
        "file_path": file_path,
        "scan_title": scan_title,
        "col_name": col_name,
        "data_slice": data_slice,
    }
