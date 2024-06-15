from os import PathLike
import pytest
import numpy
from ewoksorange.tests.utils import execute_task

from orangecontrib.ewoksxrpd.integrate1d import OWIntegrate1D
from orangecontrib.ewoksxrpd.diagnose_integrate1d import OWDiagnoseIntegrate1D
from .xrpd_theory import Measurement, Setup, xPattern, yPattern


@pytest.mark.parametrize("monitorlist", [False, True])
def test_integrate1d_task(
    tmpdir: PathLike,
    imageSetup1SampleA: Measurement,
    setup1: Setup,
    xSampleA: xPattern,
    ySampleA: yPattern,
    monitorlist: bool,
):
    assert_integrate1d(
        imageSetup1SampleA,
        setup1,
        xSampleA,
        ySampleA,
        tmpdir,
        None,
        monitorlist=monitorlist,
    )


def test_integrate1d_widget(
    tmpdir: PathLike,
    imageSetup1SampleA: Measurement,
    setup1: Setup,
    xSampleA: xPattern,
    ySampleA: yPattern,
    qtapp,
):
    assert_integrate1d(imageSetup1SampleA, setup1, xSampleA, ySampleA, tmpdir, qtapp)


# from pyFAI.method_registry import IntegrationMethod
# for method in IntegrationMethod._registry:
#    print(f"{method.split}_{method.algo}_{method.impl}")
#
# {split}_{algo}_{impl}{target}
# split: "no", "bbox", "pseudo", "full"
# algo: "histogram", "lut", "csr"
# impl: "python", "cython", "opencl"


def test_sigma_clip_task(
    tmpdir: PathLike,
    imageSetup1SampleA: Measurement,
    setup1: Setup,
    xSampleA: xPattern,
    ySampleA: yPattern,
):
    integration_options = {
        "error_model": "azimuthal",
        "method": "no_csr_cython",
        "integrator_name": "sigma_clip_ng",
        "extra_options": {"max_iter": 3, "thres": 0},
    }
    assert_integrate1d(
        imageSetup1SampleA,
        setup1,
        xSampleA,
        ySampleA,
        tmpdir,
        None,
        integration_options=integration_options,
    )


def test_sigma_clip_widget(
    tmpdir: PathLike,
    imageSetup1SampleA: Measurement,
    setup1: Setup,
    xSampleA: xPattern,
    ySampleA: yPattern,
    qtapp,
):
    integration_options = {
        "error_model": "azimuthal",
        "method": "no_csr_cython",
        "integrator_name": "sigma_clip_ng",
        "extra_options": {"max_iter": 3, "thres": 0},
    }
    assert_integrate1d(
        imageSetup1SampleA,
        setup1,
        xSampleA,
        ySampleA,
        tmpdir,
        qtapp,
        integration_options=integration_options,
    )


def test_integrate1d_reconfig(
    tmpdir: PathLike,
    imageSetup1SampleA: Measurement,
    setup1: Setup,
    imageSetup2SampleA: Measurement,
    setup2: Setup,
    xSampleA: xPattern,
    ySampleA: yPattern,
):
    assert_integrate1d(imageSetup1SampleA, setup1, xSampleA, ySampleA, tmpdir, None)
    assert_integrate1d(imageSetup2SampleA, setup2, xSampleA, ySampleA, tmpdir, None)
    assert_integrate1d(imageSetup1SampleA, setup1, xSampleA, ySampleA, tmpdir, None)
    assert_integrate1d(imageSetup1SampleA, setup1, xSampleA, ySampleA, tmpdir, None)


def assert_integrate1d(
    measurement: Measurement,
    setup: Setup,
    xpattern: xPattern,
    ypattern: yPattern,
    tmpdir: PathLike,
    qtapp,
    integration_options=None,
    monitorlist: bool = False,
):
    integration_options2 = dict(xpattern.integration_options)
    if integration_options:
        integration_options2.update(integration_options)
    inputs = {
        "image": measurement.image,
        "detector": setup.detector,
        "geometry": setup.geometry,
        "energy": setup.energy,
        "integration_options": integration_options2,
    }
    if monitorlist:
        inputs["monitors"] = [measurement.monitor, 1, None, 1]
        inputs["references"] = [ypattern.monitor, 1, 1, None]
    else:
        inputs["monitor"] = measurement.monitor
        inputs["reference"] = ypattern.monitor

    output_values = execute_task(
        OWIntegrate1D.ewokstaskclass if qtapp is None else OWIntegrate1D, inputs=inputs
    )

    assert output_values["xunits"] == xpattern.units
    numpy.testing.assert_allclose(xpattern.x, output_values["x"], rtol=1e-6)
    atol = ypattern.y.max() * 0.01
    numpy.testing.assert_allclose(ypattern.y, output_values["y"], atol=atol)

    # Set show=True to visualize the calibration results
    filename = tmpdir / "diagnose.png"
    inputs = {
        "x": output_values["x"],
        "y": output_values["y"],
        "xunits": output_values["xunits"],
        "show": False,
        "filename": str(filename),
        # "energy": setup.energy,
        # "calibrant": "LaB6"
    }
    execute_task(
        (
            OWDiagnoseIntegrate1D.ewokstaskclass
            if qtapp is None
            else OWDiagnoseIntegrate1D
        ),
        inputs=inputs,
    )
    assert filename.exists()
