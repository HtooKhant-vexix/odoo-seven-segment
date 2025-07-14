import logging
from odoo import models, api

_logger = logging.getLogger(__name__)

try:
    import serial
except ImportError:
    serial = None
    _logger.error('pyserial is not installed. Please install pyserial to use the seven segment display integration.')

class SevenSegmentDisplay(models.AbstractModel):
    _name = 'pos.seven_segment_display'
    _description = 'POS Seven Segment Display Service'

    def _send_command(self, data, port='/dev/ttyS1', baudrate=2400, command_name='Unknown'):
        if not serial:
            _logger.error('pyserial is not available.')
            return False
        try:
            ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                bytesize=8,
                parity='N',
                stopbits=1,
                timeout=1
            )
            ser.write(data)
            ser.flush()
            _logger.info(f"Sent {command_name}: {data.hex()}")
            ser.close()
            return True
        except Exception as e:
            _logger.error(f"Failed to send {command_name}: {e}")
            return False

    @api.model
    def initialize_display(self, port='/dev/ttyS1', baudrate=2400):
        """Initialize the display (ESC @)"""
        return self._send_command(bytes([27, 64]), port, baudrate, 'ESC @ (Initialize)')

    @api.model
    def clear_display(self, port='/dev/ttyS1', baudrate=2400):
        """Clear the display (CLR)"""
        return self._send_command(bytes([12]), port, baudrate, 'CLR (Clear)')

    @api.model
    def set_display_mode(self, mode, port='/dev/ttyS1', baudrate=2400):
        """Set display mode (1=Price, 2=Total, 3=Collect, 4=Change)"""
        if mode not in [1, 2, 3, 4]:
            _logger.error(f"Invalid display mode: {mode}")
            return False
        return self._send_command(bytes([27, 115, 48 + mode]), port, baudrate, f'ESC s {mode} (Set Mode)')

    @api.model
    def display_value(self, value, port='/dev/ttyS1', baudrate=2400):
        """Display a value on the screen"""
        try:
            formatted_value = f"{float(value):.2f}"
        except Exception as e:
            _logger.error(f"Invalid value for display: {value} ({e})")
            return False
        if len(formatted_value.replace('.', '')) > 15:
            formatted_value = f"{float(value):.7f}"
        data = bytes([27, 81, 65]) + formatted_value.encode('ascii') + bytes([13])
        return self._send_command(data, port, baudrate, f'ESC Q A {formatted_value} CR (Display Data)')
