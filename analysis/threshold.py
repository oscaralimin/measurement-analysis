import logging
import numpy as np
from typing import Dict, List, Tuple

from core.types import ChannelConfig, AnalysisResult

class ThresholdAnalyzer:
    """
    Analyzes measurement data against defined thresholds.
    Handles both static and dynamic threshold comparisons.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def analyze(self, channel_data: np.ndarray, timestamps: np.ndarray, 
                config: ChannelConfig) -> AnalysisResult:
        """
        Analyzes channel data against thresholds.
        
        Args:
            channel_data: Array of measurement values
            timestamps: Array of corresponding timestamps
            config: Channel configuration
            
        Returns:
            AnalysisResult containing analysis results
        """
        self.logger.info(f"Analyzing channel: {config.name}")
        
        try:
            if config.setpoint_channel:
                violations = self._check_dynamic_threshold(
                    channel_data, timestamps, config)
            else:
                violations = self._check_static_threshold(
                    channel_data, timestamps, config)
            
            max_deviation = self._calculate_max_deviation(violations)
            
            return AnalysisResult(
                channel_name=config.name,
                passed=len(violations) == 0,
                violations=violations,
                max_deviation=max_deviation
            )
            
        except Exception as e:
            self.logger.error(f"Analysis failed for {config.name}: {str(e)}")
            raise

    def _check_static_threshold(self, data: np.ndarray, timestamps: np.ndarray, 
                              config: ChannelConfig) -> List[Tuple[float, float, float]]:
        """
        Checks data against static threshold.
        
        Returns:
            List of (timestamp, value, deviation) for violations
        """
        violations = []
        setpoint = float(config.static_setpoint)
        tolerance = float(config.static_tolerance)
        
        upper_bound = setpoint + tolerance
        lower_bound = setpoint - tolerance
        
        for t, v in zip(timestamps, data):
            if v > upper_bound or v < lower_bound:
                deviation = max(v - upper_bound, lower_bound - v)
                violations.append((t, v, deviation))
                
        return violations

    def _check_dynamic_threshold(self, data: np.ndarray, timestamps: np.ndarray,
                               setpoint_data: np.ndarray, config: ChannelConfig
                               ) -> List[Tuple[float, float, float]]:
        """
        Checks data against dynamic threshold from setpoint channel.
        
        Returns:
            List of (timestamp, value, deviation) for violations
        """
        violations = []
        tolerance = float(config.static_tolerance)
        
        for t, v, s in zip(timestamps, data, setpoint_data):
            upper_bound = s + tolerance
            lower_bound = s - tolerance
            
            if v > upper_bound or v < lower_bound:
                deviation = max(v - upper_bound, lower_bound - v)
                violations.append((t, v, deviation))
                
        return violations

    def _calculate_max_deviation(self, violations: List[Tuple[float, float, float]]) -> float:
        """Calculates maximum deviation from violations list."""
        if not violations:
            return 0.0
        return max(v[2] for v in violations)