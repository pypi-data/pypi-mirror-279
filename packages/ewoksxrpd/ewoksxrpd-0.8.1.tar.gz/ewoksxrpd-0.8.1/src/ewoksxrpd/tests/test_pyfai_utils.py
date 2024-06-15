from ..tasks.utils import pyfai_utils


def test_normalize_parameters():
    parameters = {
        "key1": 10,
        "key2": "normal",
        "key3": [
            "/gpfs/jazzy",
            "/gpfs/jazzy/",
            "silx:///gpfs/jazzy/path/to/file",
            "/mnt/multipath-shares/path/to/file",
        ],
    }
    parameters["key4"] = {
        "key1": 10,
        "key2": "normal",
        "key3": [
            "/gpfs/jazzy",
            "/gpfs/jazzy/",
            "silx:///gpfs/jazzy/path/to/file",
            "/mnt/multipath-shares/path/to/file",
        ],
    }
    normalized = {
        "key1": 10,
        "key2": "normal",
        "key3": ["/gpfs/jazzy", "/", "silx:///path/to/file", "/path/to/file"],
    }
    normalized["key4"] = {
        "key1": 10,
        "key2": "normal",
        "key3": ["/gpfs/jazzy", "/", "silx:///path/to/file", "/path/to/file"],
    }
    assert pyfai_utils.normalize_parameters(parameters) == normalized
