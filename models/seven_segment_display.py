# Copyright (C) 2025 Htoo Aung Khant
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
