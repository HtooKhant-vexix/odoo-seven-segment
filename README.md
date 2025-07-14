# POS Seven Segment Display Integration

This custom Odoo module integrates an OCPD-LED8 seven segment display with the Point of Sale (POS) system. It allows the POS to display product prices, totals, collected amounts, change, and more in real time on the external display.

## Features
- Display product price when a product is added or its quantity/price/discount is changed
- Show order total when entering the payment screen
- Show collected amount in 'Collect' mode when entering payment
- Show change after payment is finalized
- Reset display to `0.00` when starting a new order
- Fully configurable serial port and baudrate

## Installation
1. Copy the `pos_seven_segment_display` module directory into your Odoo `addons` folder.
2. Install the module from the Odoo Apps menu (search for "POS Seven Segment Display").
3. Ensure the Python package `pyserial` is installed on your Odoo server:
   ```bash
   pip install pyserial
   ```

## Configuration
- By default, the display uses serial port `/dev/ttyS1` and baudrate `2400`.
- 
- **Configuration Location in Code:**
- - The default serial port and baudrate are set in the backend Python file:
-   - `pos_seven_segment_display/models/seven_segment_display.py`
-   - Look for the methods: `_send_command`, `initialize_display`, `clear_display`, `set_display_mode`, and `display_value`.
-   - Each of these methods has `port='/dev/ttyS1'` and `baudrate=2400` as default arguments.
-   - To change the defaults, edit these arguments in the code.
-   - Example:

  ```python
  def _send_command(self, data, port='/dev/ttyS1', baudrate=2400, command_name='Unknown'):
  ```
-   - You can also override the port and baudrate by passing them as parameters when calling these methods from other modules or endpoints.
- The display must be physically connected to the Odoo server's serial port.
- The Odoo server user must have permission to access the serial port (usually by being in the `dialout` group).

## Usage
### POS Flow
- **Add Product:** The display shows the product price (unit price × quantity × (1 - discount/100)).
- **Change Quantity/Discount/Price:** The display updates to show the new line price.
- **Click Payment:** The display switches to 'Total' mode and shows the order total.
- **Enter Collected Amount:** The display switches to 'Collect' mode and shows the collected value.
- **Finalize Payment:** The display switches to 'Change' mode and shows the change due.
- **New Order:** The display resets to show `0.00`.

### Backend Endpoints
The module exposes the following JSON endpoints (all require authentication):
- `/pos_seven_segment_display/initialize` — Initialize the display
- `/pos_seven_segment_display/clear` — Clear the display
- `/pos_seven_segment_display/set_mode` — Set display mode (1=Price, 2=Total, 3=Collect, 4=Change)
- `/pos_seven_segment_display/display_value` — Display a value

### Frontend Integration
- The module provides a frontend service (`seven_segment_display`) that is used by the POS UI to send display updates.
- All display updates are triggered automatically by POS events (product add, quantity/discount/price change, payment, etc.).

## Troubleshooting
- **Permission Denied on Serial Port:**
  - Add the Odoo server user to the `dialout` group:
    ```bash
    sudo usermod -a -G dialout <odoo_user>
    ```
  - give permission to serail port:
    ```bash
    sudo chmod -R 777 /dev/ttyS1
    ```
  - Restart the server or log out/in.
- **Display Not Updating:**
  - Check Odoo logs for errors.
  - Ensure the display is connected and powered.
  - Ensure the correct serial port and baudrate are used.

## Customization
- You can change the display logic (e.g., show subtotal, custom messages) by editing the relevant JS files in the POS module.
- The backend logic can be extended to support other display models or protocols.

## Authors
- Htoo Aung Khant

## License
- AGPL-3.0