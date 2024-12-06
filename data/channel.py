import numpy as np
from typing import Dict, Any, Optional, Tuple

class Channel:
    def __init__(self, name: str, data: np.ndarray, timestamps: np.ndarray, 
                 metadata: Optional[Dict[str, Any]] = None):
        self.name = name
        self.data = data
        self.timestamps = timestamps
        self.metadata = metadata or {}
        self._validate_data()

    def _validate_data(self) -> None:
        if len(self.data) != len(self.timestamps):
            raise ValueError(
                f"Data length ({len(self.data)}) doesn't match timestamps "
                f"length ({len(self.timestamps)})")

    def get_timerange(self, start: Optional[float] = None, 
                     end: Optional[float] = None) -> Tuple[np.ndarray, np.ndarray]:
        mask = np.ones(len(self.timestamps), dtype=bool)
        
        if start is not None:
            mask &= (self.timestamps >= start)
        if end is not None:
            mask &= (self.timestamps <= end)
            
        return self.data[mask], self.timestamps[mask]

    def scale(self, factor: float) -> None:
        if factor != 1.0:
            self.data *= factor