import logging
from typing import Dict, Any

class ConfigValidator:
    """
    Validates configuration data for measurement channels.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Define required fields and their types
        self.required_fields = {
            "Sollwertkanal": str,
            "Toleranz statisch": (float, str),
            "Skalierung": (float, str),
            "back2backID": str,
            "back2backIDPosition": (int, str)
        }

    def validate_channel_config(self, channel_name: str, config: Dict[str, Any]) -> bool:
        """
        Validates configuration for a single channel.
        
        Args:
            channel_name: Name of the channel
            config: Dictionary containing channel configuration
            
        Returns:
            bool: True if configuration is valid, False otherwise
        """
        try:
            # Check all required fields are present
            for field in self.required_fields:
                if field not in config:
                    self.logger.error(f"Missing required field '{field}' for channel {channel_name}")
                    return False

            # Validate field types and values
            if not self._validate_setpoint_config(channel_name, config):
                return False

            if not self._validate_numeric_fields(channel_name, config):
                return False

            if not self._validate_test_flags(channel_name, config):
                return False

            return True

        except Exception as e:
            self.logger.error(f"Validation error for channel {channel_name}: {str(e)}")
            return False

    def _validate_setpoint_config(self, channel_name: str, config: Dict[str, Any]) -> bool:
        """Validates setpoint configuration."""
        has_setpoint_channel = bool(config["Sollwertkanal"])
        has_static_setpoint = bool(config.get("Sollwert statisch"))

        if has_setpoint_channel and has_static_setpoint:
            self.logger.warning(
                f"Channel {channel_name} has both dynamic and static setpoints configured. "
                "Using dynamic setpoint."
            )

        if not (has_setpoint_channel or has_static_setpoint):
            self.logger.error(
                f"Channel {channel_name} has no setpoint configured. "
                "Either Sollwertkanal or Sollwert statisch must be specified."
            )
            return False

        return True

    def _validate_numeric_fields(self, channel_name: str, config: Dict[str, Any]) -> bool:
        """Validates numeric fields in configuration."""
        try:
            # Validate tolerance
            if config["Toleranz statisch"]:
                tolerance = float(config["Toleranz statisch"])
                if tolerance < 0:
                    self.logger.error(f"Negative tolerance not allowed for channel {channel_name}")
                    return False

            # Validate scaling
            if config["Skalierung"]:
                scaling = float(config["Skalierung"])
                if scaling <= 0:
                    self.logger.error(f"Scaling must be positive for channel {channel_name}")
                    return False

            # Validate back2backIDPosition
            if config["back2backIDPosition"]:
                position = int(config["back2backIDPosition"])
                if position < 0:
                    self.logger.error(f"Invalid back2backIDPosition for channel {channel_name}")
                    return False

            return True

        except ValueError as e:
            self.logger.error(f"Invalid numeric value in configuration for channel {channel_name}: {str(e)}")
            return False

    def _validate_test_flags(self, channel_name: str, config: Dict[str, Any]) -> bool:
        """Validates test flag configuration if present."""
        if config.get("Testflagchannel"):
            if not config.get("Testflag"):
                self.logger.error(f"Test flag channel specified but no flag value for {channel_name}")
                return False
            try:
                flag = int(config["Testflag"])
                if flag < 0:
                    self.logger.error(f"Invalid test flag value for channel {channel_name}")
                    return False
            except ValueError:
                self.logger.error(f"Test flag must be an integer for channel {channel_name}")
                return False
        return True