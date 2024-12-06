import logging
from pathlib import Path
from typing import Dict, List, Optional
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

class ChannelPlotter:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.colors = {
            'data': 'blue',
            'threshold': 'red',
            'violation': 'red',
            'setpoint': 'green'
        }

    def create_plot(self, channel_name: str, data: np.ndarray, 
                   timestamps: np.ndarray, config: Dict, 
                   violations: List[Dict]) -> Figure:
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Plot main data
        ax.plot(timestamps, data, color=self.colors['data'], 
                label='Measured', linewidth=0.5)
        
        # Plot thresholds
        if config.get('setpoint_channel'):
            self._add_dynamic_thresholds(ax, timestamps, data, config)
        else:
            self._add_static_thresholds(ax, timestamps, config)
        
        # Highlight violations
        self._add_violations(ax, violations)
        
        # Setup labels and title
        self._setup_plot(ax, channel_name, config)
        
        return fig

    def _add_dynamic_thresholds(self, ax, timestamps: np.ndarray, 
                              setpoint_data: np.ndarray, config: Dict) -> None:
        tolerance = float(config['Toleranz statisch'])
        ax.plot(timestamps, setpoint_data + tolerance, 
                color=self.colors['threshold'], 
                linestyle='--', label='Upper Threshold')
        ax.plot(timestamps, setpoint_data - tolerance, 
                color=self.colors['threshold'], 
                linestyle='--', label='Lower Threshold')

    def _add_static_thresholds(self, ax, timestamps: np.ndarray, 
                             config: Dict) -> None:
        setpoint = float(config['Sollwert statisch'])
        tolerance = float(config['Toleranz statisch'])
        
        ax.axhline(y=setpoint + tolerance, color=self.colors['threshold'], 
                   linestyle='--', label='Upper Threshold')
        ax.axhline(y=setpoint - tolerance, color=self.colors['threshold'], 
                   linestyle='--', label='Lower Threshold')

    def _add_violations(self, ax, violations: List[Dict]) -> None:
        for violation in violations:
            ax.axvspan(violation['timestamp'] - 0.1, 
                      violation['timestamp'] + 0.1,
                      color=self.colors['violation'], 
                      alpha=0.3)

    def _setup_plot(self, ax, channel_name: str, config: Dict) -> None:
        ax.set_xlabel('Time (s)')
        ax.set_ylabel(f'{channel_name} ({config.get("unit", "")})')
        ax.grid(True)
        ax.legend()