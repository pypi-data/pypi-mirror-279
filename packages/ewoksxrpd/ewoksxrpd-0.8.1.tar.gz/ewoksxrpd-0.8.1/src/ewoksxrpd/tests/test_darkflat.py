from typing import Optional
import numpy

from ..tasks.integrate import Integrate1D
from .xrpd_theory import Measurement, Setup, xPattern, yPattern


def test_flatdark_task(
    imageSetup1SampleA: Measurement,
    setup1: Setup,
    xSampleA: xPattern,
    ySampleA: yPattern,
):
    image = imageSetup1SampleA.image
    assert_integrate1d(
        image,
        imageSetup1SampleA.monitor,
        setup1,
        xSampleA,
        ySampleA,
    )

    imax = image.max()
    flatfield = numpy.random.uniform(low=imax * 0.9, high=imax * 1.5, size=image.shape)
    darkcurrent = numpy.random.uniform(low=0, high=imax * 0.1, size=image.shape)

    # Flat/dark correction (pyFAI):
    #  Icor = (I - dark) / flat
    image = flatfield * image + darkcurrent
    assert_integrate1d(
        image,
        imageSetup1SampleA.monitor,
        setup1,
        xSampleA,
        ySampleA,
        flatfield=flatfield,
        darkcurrent=darkcurrent,
    )

    # Flat/dark correction (counts):
    #  Icor = (I - dark) / max(flat - dark, 1)
    assert_integrate1d(
        image,
        imageSetup1SampleA.monitor,
        setup1,
        xSampleA,
        ySampleA,
        flatfield=flatfield + darkcurrent,
        darkcurrent=darkcurrent,
        darkflatmethod="counts",
    )


def assert_integrate1d(
    image: numpy.ndarray,
    monitor: float,
    setup: Setup,
    xpattern: xPattern,
    ypattern: yPattern,
    flatfield: Optional[numpy.ndarray] = None,
    darkcurrent: Optional[numpy.ndarray] = None,
    **custom_integration_options
):
    integration_options = dict(xpattern.integration_options)
    integration_options.update(custom_integration_options)
    inputs = {
        "image": image,
        "detector": setup.detector,
        "geometry": setup.geometry,
        "energy": setup.energy,
        "monitor": monitor,
        "reference": ypattern.monitor,
        "integration_options": integration_options,
        "flatfield": flatfield,
        "darkcurrent": darkcurrent,
    }

    task = Integrate1D(inputs=inputs)
    task.execute()
    output_values = task.get_output_values()

    assert output_values["xunits"] == xpattern.units
    numpy.testing.assert_allclose(xpattern.x, output_values["x"], rtol=1e-6)
    atol = ypattern.y.max() * 0.01
    numpy.testing.assert_allclose(ypattern.y, output_values["y"], atol=atol)
