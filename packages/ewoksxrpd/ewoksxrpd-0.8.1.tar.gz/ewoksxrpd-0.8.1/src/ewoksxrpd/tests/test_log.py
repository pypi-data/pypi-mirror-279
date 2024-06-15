import logging
from ewoksxrpd.tasks.log import zip_with_progress


def test_zip_with_progress(caplog):
    with caplog.at_level(logging.INFO):
        values = list()
        for value in zip_with_progress([], message="Integrated %s images of %s"):
            values.append(value)

    assert not values
    assert "Integrated 0 images of ? (FINISHED)" in caplog.text

    with caplog.at_level(logging.INFO):
        values = list()
        for (value,) in zip_with_progress([1], message="Integrated %s images of %s"):
            values.append(value)

    assert values == [1]
    assert "Integrated 1 images of ? (FINISHED)" in caplog.text

    with caplog.at_level(logging.INFO):
        values = list()
        for value, *_ in zip_with_progress(
            [1, 2], message="Integrated %s images of %s"
        ):
            values.append(value)

    assert values == [1, 2]
    assert "Integrated 2 images of ? (FINISHED)" in caplog.text

    with caplog.at_level(logging.INFO):
        values = list()
        for nr, letter in zip_with_progress(
            [1, 2],
            [
                "a",
            ],
            message="Integrated %s images of %s",
        ):
            values.append((nr, letter))

    assert values == [(1, "a")]
    assert "Integrated 1 images of ? (FINISHED)" in caplog.text
