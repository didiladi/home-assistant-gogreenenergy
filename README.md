# GoGreenEnergy Home Assistant Integration

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This custom integration provides a sensor for **GoGreenEnergy** electricity and gas prices directly in Home Assistant. Track your real-time spot market and flexible tariffs easily!

## Features

- 🔌 Fetches current and historical energy prices for GoGreenEnergy products (electricity/gas).
- ⚙️ Supports various tariff options like `plus` and `future`.
- 💶 Calculates costs inclusive of VAT.
- ⚡ Configurable tracking of your **Full Energy Costs** by allowing you to add grid fees and handling fees (Abwicklungsgebühr).
- 🕒 Respectful polling: Updates price data once per hour to avoid unnecessary API calls.

---

## Installation

### Method 1: HACS (Recommended)

This integration is fully compatible with [HACS (Home Assistant Community Store)](https://hacs.xyz/).

1. Open HACS in your Home Assistant instance.
2. Click on the 3 dots in the top right corner and select **Custom repositories**.
3. Add the URL to this repository (`https://github.com/didiladi/home-assistant-gogreenenergy`) and select **Integration** as the category.
4. Click **Add**.
5. You should now see "GoGreenEnergy" in your HACS integrations list. Click on it and select **Download**.
6. Restart Home Assistant.

### Method 2: Manual Installation

1. Download this repository.
2. Copy the `custom_components/gogreenenergy` folder into your Home Assistant `custom_components` directory.
3. Restart Home Assistant.

---

## Configuration

### Method 1: UI Setup (Recommended)

1. In Home Assistant, go to **Settings** -> **Devices & Services**.
2. Click **Add Integration** in the bottom right corner.
3. Search for **GoGreenEnergy** and select it.
4. Fill out the configuration form:
   - **Product Key**: The specific GoGreenEnergy product key you are tracking (e.g., `GSFLEX`).
   - **Include 'plus' / 'future' options**: Check these boxes if your tariff includes them.
   - **Additional Fee per kWh**: A flat fee in EUR/kWh added to your price. Use this to track the GoGreen handling fee (e.g. `0.015`) and/or your regional grid fees.
5. Click **Submit**. You're done! No restarts required.

### Method 2: YAML Configuration (Legacy)

If you prefer `configuration.yaml`, you can add the following:

```yaml
sensor:
  - platform: gogreenenergy
    product_key: GSFLEX
    options:
      - plus
    additional_fee_per_kwh: 0.015
```

### Configuration Variables

| Variable | Type | Required | Default | Description |
| -------- | ---- | -------- | ------- | ----------- |
| `platform` | string | **Yes** | `gogreenenergy` | Must be `gogreenenergy`. |
| `product_key` | string | No | `GSFLEX` | The specific GoGreenEnergy product key you are tracking. |
| `options` | list | No | `['plus']` | A list of specific tariff options (e.g., `plus`, `future`). |
| `additional_fee_per_kwh` | float | No | `0.015` | A flat fee in EUR/kWh added to your price. |

### Tracking Your Full Energy Costs

The basic GoGreen API provides the bare `energyPrice`. To properly track the costs hitting your wallet, use the `additional_fee_per_kwh` parameter:

- **GoGreenEnergy Handling Fee (Abwicklungsgebühr)**: For Flex tariffs, GoGreen usually adds a handling fee (often around 1.5 cents/kWh gross). The default value is set to `0.015`.
- **Grid Fees and Taxes (Netzkosten & Abgaben)**: If you get a combined bill and want to track the *absolute* full cost of electricity, calculate your regional grid fee + taxes per kWh (e.g., 6.5 cents) and add it to the GoGreen handling fee. Set `additional_fee_per_kwh: 0.08` (for 8 cents total).

---

## Contributing

Contributions are always welcome! Please read the [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

Created by [@didiladi](https://github.com/didiladi)