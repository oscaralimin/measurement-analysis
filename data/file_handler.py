import logging
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import numpy as np
import asammdf

from .channel import Channel

class FileHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.cache: Dict[str, asammdf.MDF] = {}

    def load_mf4(self, file_path: Path) -> asammdf.MDF:
        try:
            if str(file_path) in self.cache:
                return self.cache[str(file_path)]
            
            self.logger.info(f"Loading MF4 file: {file_path}")
            mdf = asammdf.MDF(file_path, use_display_names=False)
            mdf.configure(integer_interpolation=0, float_interpolation=0)
            
            self.cache[str(file_path)] = mdf
            return mdf
            
        except Exception as e:
            self.logger.error(f"Failed to load MF4 file: {str(e)}")
            raise

    def filter_channels(self, mdf: asammdf.MDF, config: Dict[str, Dict]) -> Dict[str, Channel]:
        channels = {}
        for channel_name, channel_config in config.items():
            try:
                channel_data = self._extract_channel(mdf, channel_name, channel_config)
                if channel_data:
                    channels[channel_name] = channel_data
            except Exception as e:
                self.logger.error(f"Failed to extract channel {channel_name}: {str(e)}")
                raise

        return channels

    def _extract_channel(self, mdf: asammdf.MDF, channel_name: str, config: Dict) -> Optional[Channel]:
        occurrences = mdf.whereis(channel_name)
        
        if not occurrences:
            self.logger.error(f"Channel {channel_name} not found")
            return None

        if len(occurrences) == 1:
            # Get the group and index from the occurrence tuple
            group, index = occurrences[0]
            signal = mdf.get(group=group, index=index)
        else:
            signal = self._find_channel_by_id(mdf, occurrences, config)
            
        if signal is None:
            return None
            
        return Channel(
            name=channel_name,
            data=signal.samples,
            timestamps=signal.timestamps,
            metadata={'source': signal.source}
        )
    
    def _find_channel_by_id(self, mdf: asammdf.MDF, occurrences: List[Tuple], 
                           config: Dict) -> Optional[asammdf.Signal]:
        back2back_id = config.get('back2backID', '')
        
        for occ in occurrences:
            signal = mdf.get(group=occ[0], index=occ[1])
            if back2back_id in signal.source.name:
                return signal
                
        return None