from typing import List, Optional, Dict, Any
from datetime import datetime

class ChannelConfig:
    """Configuration settings for a measurement channel."""
    
    def __init__(self, name: str):
        self.name = name
        self.setpoint_channel: Optional[str] = None
        self.static_setpoint: Optional[float] = None
        self.static_tolerance: float = 0.0
        self.scaling: float = 1.0
        self.back2back_id: str = ""
        self.back2back_id_position: int = 0
        self.unit: str = ""
        self.test_flag_channel: Optional[str] = None
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.test_flag: Optional[int] = None

class AnalysisResult:
    """Results from analyzing a measurement channel."""
    
    def __init__(self, channel_name: str):
        self.channel_name = channel_name
        self.passed: bool = False
        self.violations: List[Dict[str, float]] = []
        self.max_deviation: float = 0.0
        self.analysis_time: datetime = datetime.now()
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
        self.statistics: Dict[str, Any] = {}

    def add_violation(self, timestamp: float, value: float, deviation: float) -> None:
        """Add a threshold violation."""
        self.violations.append({
            'timestamp': timestamp,
            'value': value,
            'deviation': deviation
        })
        self.max_deviation = max(self.max_deviation, abs(deviation))

    def calculate_statistics(self) -> None:
        """Calculate basic statistics for the analysis."""
        if self.violations:
            self.statistics.update({
                'total_violations': len(self.violations),
                'max_deviation': self.max_deviation,
                'violation_times': [v['timestamp'] for v in self.violations]
            })