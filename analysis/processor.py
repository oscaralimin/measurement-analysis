import logging
import numpy as np
from typing import Dict, Tuple

from core.types import ChannelConfig

class DataProcessor:
    """
    Processes raw measurement data before analysis.
    Handles scaling, filtering, and time window selection.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def process_channel(self, data: np.ndarray, timestamps: np.ndarray, 
                       config: ChannelConfig) -> Tuple[np.ndarray, np.ndarray]:
        """
        Applies all necessary processing to channel data.
        
        Args:
            data: Raw measurement data
            timestamps: Corresponding timestamps
            config: Channel configuration
            
        Returns:
            Tuple of (processed_data, processed_timestamps)
        """
        try:
            # Apply scaling if specified
            if config.scaling != 1.0:
                data = self._apply_scaling(data, config.scaling)
                
            # Apply time window if specified
            if config.start_time is not None or config.end_time is not None:
                data, timestamps = self._apply_time_window(
                    data, timestamps, config.start_time, config.end_time)
                
            return data, timestamps
            
        except Exception as e:
            self.logger.error(f"Processing failed for {config.name}: {str(e)}")
            raise

    def _apply_scaling(self, data: np.ndarray, scaling: float) -> np.ndarray:
        """Applies scaling factor to data."""
        return data * scaling

    def _apply_time_window(self, data: np.ndarray, timestamps: np.ndarray,
                          start_time: float = None, end_time: float = None
                          ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Selects data within specified time window.
        
        Returns:
            Tuple of (windowed_data, windowed_timestamps)
        """
        mask = np.ones(len(timestamps), dtype=bool)
        
        if start_time is not None:
            mask &= (timestamps >= start_time)
        if end_time is not None:
            mask &= (timestamps <= end_time)
            
        return data[mask], timestamps[mask]

    def interpolate_channel(self, data: np.ndarray, timestamps: np.ndarray, 
                          target_timestamps: np.ndarray) -> np.ndarray:
        """
        Interpolates channel data to match target timestamps.
        
        Returns:
            Interpolated data array
        """
        return np.interp(target_timestamps, timestamps, data)