import dataclasses
from json import JSONEncoder

import numpy as np


class PriceCypherJsonEncoder(JSONEncoder):
    """
    JSON encoder that can properly serialize dataclasses and numpy numbers.
    """
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        elif dataclasses.is_dataclass(obj):
            return dataclasses.asdict(obj)
        elif isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()

        return super().default(obj)
