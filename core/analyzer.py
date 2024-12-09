import logging
from pathlib import Path
from typing import Dict, Any
import numpy as np

from config.config_handler import ConfigHandler
from data import FileHandler
from analysis import ThresholdAnalyzer, DataProcessor
from .types import ChannelConfig, AnalysisResult

class MeasurementAnalyzer:
    """
    Main class coordinating the measurement analysis process.
    Handles configuration, data loading, and analysis coordination.
    """
    
    def __init__(self, config_file: Path):
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.config_handler = ConfigHandler(config_file)
        self.file_handler = FileHandler()
        self.data_processor = DataProcessor()
        self.threshold_analyzer = ThresholdAnalyzer()
        
        # Store configurations and results
        self.config: Dict[str, ChannelConfig] = {}
        self.results: Dict[str, AnalysisResult] = {}
        self.channels: Dict[str, Dict[str, np.ndarray]] = {}

    def analyze_file(self, mf4_file: Path) -> Dict[str, AnalysisResult]:
        """
        Analyzes a single MF4 file for all configured channels.
        
        Args:
            mf4_file: Path to the MF4 file to analyze
            
        Returns:
            Dictionary of analysis results for each channel
        """
        try:
            self.logger.info(f"Starting analysis of {mf4_file}")
            
            # Load and filter channels
            mf4_data = self.file_handler.load_mf4(mf4_file)
            channels = self.file_handler.filter_channels(
                mf4_data, 
                self.config_handler.config
            )
            
            # Process each channel
            for channel_name, config in self.config_handler.config.items():
                try:
                    result = self._analyze_channel(channel_name, channels, config)
                    self.results[channel_name] = result
                    
                except Exception as e:
                    self.logger.error(f"Failed to analyze channel {channel_name}: {str(e)}")
                    continue
            
            return self.results
            
        except Exception as e:
            self.logger.error(f"Analysis failed: {str(e)}")
            raise

    def _analyze_channel(self, channel_name: str, channels: Dict[str, np.ndarray], 
                        config: Dict[str, Any]) -> AnalysisResult:
        """
        Analyzes a single channel.
        
        Args:
            channel_name: Name of the channel
            channels: Dictionary of channel data
            config: Channel configuration
            
        Returns:
            Analysis results for the channel
        """
        # Create configuration object
        channel_config = self._create_channel_config(channel_name, config)
        
        # Get and process channel data
        data, timestamps = self.data_processor.process_channel(
            channels[channel_name]['data'],
            channels[channel_name]['timestamps'],
            channel_config
        )
        
        # Store processed channel data
        self.channels[channel_name] = {
            'data': data,
            'timestamps': timestamps
        }
        
        # Analyze against thresholds
        result = self.threshold_analyzer.analyze(
            data, timestamps, channel_config
        )
        
        # Calculate additional statistics
        result.calculate_statistics()
        
        return result

    def _create_channel_config(self, channel_name: str, 
                             config_data: Dict[str, Any]) -> ChannelConfig:
        """Creates a ChannelConfig object from configuration data."""
        config = ChannelConfig(channel_name)
        
        # Set basic configuration
        config.setpoint_channel = config_data.get('Sollwertkanal', '')
        config.static_tolerance = float(config_data.get('Toleranz statisch', 0))
        config.scaling = float(config_data.get('Skalierung', 1))
        
        # Set identification parameters
        config.back2back_id = config_data.get('back2backID', '')
        config.back2back_id_position = int(config_data.get('back2backIDPosition', 0))
        
        # Set test parameters
        if 'Testflagchannel' in config_data:
            config.test_flag_channel = config_data['Testflagchannel']
            config.test_flag = int(config_data.get('Testflag', 0))
        
        # Set timing parameters
        if 'startTime' in config_data:
            config.start_time = float(config_data['startTime'])
        if 'endTime' in config_data:
            config.end_time = float(config_data['endTime'])
        
        return config