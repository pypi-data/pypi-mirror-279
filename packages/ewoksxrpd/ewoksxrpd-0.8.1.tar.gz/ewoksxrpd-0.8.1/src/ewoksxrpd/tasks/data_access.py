from contextlib import contextmanager
from typing import Iterator, Union
import numpy
import h5py
from silx.io.url import DataUrl
from silx.io import h5py_utils
from ewokscore import TaskWithProgress
from ewoksdata.data import nexus
from ewoksdata.data import bliss
from .utils import data_utils


class TaskWithDataAccess(
    TaskWithProgress,
    optional_input_names=["retry_timeout", "retry_period"],
    register=False,
):
    def get_retry_options(self):
        retry_timeout = self.get_input_value("retry_timeout", None)
        retry_period = self.get_input_value("retry_period", None)
        return {"retry_timeout": retry_timeout, "retry_period": retry_period}

    @contextmanager
    def open_h5item(
        self, url: Union[str, DataUrl], create: bool = False, **openoptions
    ) -> Iterator[Union[h5py.Group, h5py.Dataset, numpy.ndarray]]:
        if isinstance(url, DataUrl):
            url = DataUrl(url)
        retryoptions = self.get_retry_options()
        if create:
            url = nexus.create_url(url, **retryoptions)
        with h5py_utils.open_item(
            url.file_path(), url.data_path(), **retryoptions, **openoptions
        ) as item:
            idx = url.data_slice()
            if idx is None:
                yield item
            else:
                yield item[idx]

    def get_data(self, *args, **kw):
        kw.update(self.get_retry_options())
        return bliss.get_data(*args, **kw)

    def get_image(self, *args, **kw):
        kw.update(self.get_retry_options())
        return bliss.get_image(*args, **kw)

    def iter_bliss_data(self, *args, **kw):
        kw.update(self.get_retry_options())
        yield from bliss.iter_bliss_scan_data(*args, **kw)

    def iter_bliss_data_from_memory(self, *args, **kw):
        kw.update(self.get_retry_options())
        yield from bliss.iter_bliss_scan_data_from_memory(*args, **kw)

    def link_bliss_scan(self, *args, **kw):
        kw.update(self.get_retry_options())
        return data_utils.link_bliss_scan(*args, **kw)
