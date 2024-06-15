import time

from src.core.utils import log
from src.models.base.params import Params


@log
def pipeline(params: Params) -> dict:
    try:
        time.sleep(5)
        return {f"prediction": str(params)}
    except Exception as error:
        raise(error)
