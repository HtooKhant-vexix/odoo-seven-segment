from odoo import http
from odoo.http import request

class SevenSegmentDisplayController(http.Controller):
    @http.route('/pos_seven_segment_display/initialize', type='json', auth='user')
    def initialize_display(self, port='/dev/ttyS1', baudrate=2400):
        result = request.env['pos.seven_segment_display'].sudo().initialize_display(port, baudrate)
        return {'success': result}

    @http.route('/pos_seven_segment_display/clear', type='json', auth='user')
    def clear_display(self, port='/dev/ttyS1', baudrate=2400):
        result = request.env['pos.seven_segment_display'].sudo().clear_display(port, baudrate)
        return {'success': result}

    @http.route('/pos_seven_segment_display/set_mode', type='json', auth='user')
    def set_display_mode(self, mode, port='/dev/ttyS1', baudrate=2400):
        result = request.env['pos.seven_segment_display'].sudo().set_display_mode(mode, port, baudrate)
        return {'success': result}

    @http.route('/pos_seven_segment_display/display_value', type='json', auth='user')
    def display_value(self, value, port='/dev/ttyS1', baudrate=2400):
        result = request.env['pos.seven_segment_display'].sudo().display_value(value, port, baudrate)
        return {'success': result}
