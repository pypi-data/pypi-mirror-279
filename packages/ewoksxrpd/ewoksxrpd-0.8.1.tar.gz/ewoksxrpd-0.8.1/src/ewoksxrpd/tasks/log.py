import time
import logging
from typing import Iterator, Optional, Any, Tuple, Generator

_logger = logging.getLogger(__name__)


def zip_with_progress(
    *iterators: Iterator[Iterator[Any]],
    message: str = "Progress %d/%s",
    nmax: Optional[int] = None,
    period: float = 5,
    logger=None,
) -> Generator[Tuple[Any], None, None]:
    """Like python's zip but will progress logging when iterating over the result."""
    if logger is None:
        logger = _logger
    i = 0
    t0 = time.time()
    if nmax is None:
        nmax = "?"
    try:
        for tpl in zip(*iterators):
            yield tpl
            i += 1
            if (time.time() - t0) > period:
                t0 = time.time()
                _logger.info(message, i, nmax)
    finally:
        _logger.info(f"{message} (FINISHED)", i, nmax)
