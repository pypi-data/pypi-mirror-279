import os
import numpy
from ewokscore import Task

from .utils.data_utils import is_data
from .utils.pyfai_utils import integration_info_as_text

__all__ = ["SaveAsciiPattern1D"]


class SaveAsciiPattern1D(
    Task,
    input_names=["filename", "x", "y", "xunits"],
    optional_input_names=["header", "yerror", "metadata"],
    output_names=["saved"],
):
    """Save single diffractogram in ASCII format"""

    def run(self):
        if is_data(self.inputs.yerror):
            data = [self.inputs.x, self.inputs.y, self.inputs.yerror]
            columns = ["x", "intensity", "intensity_error"]
        else:
            data = [self.inputs.x, self.inputs.y]
            columns = ["x", "intensity"]
        data = numpy.stack(data, axis=1)

        header = self.get_input_value("header", dict())
        metadata = self.get_input_value("metadata", dict())
        lines = integration_info_as_text(header, xunits=self.inputs.xunits, **metadata)
        lines.append(" ".join(columns))

        dirname = os.path.dirname(self.inputs.filename)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        numpy.savetxt(self.inputs.filename, data, header="\n".join(lines))
        self.outputs.saved = True
