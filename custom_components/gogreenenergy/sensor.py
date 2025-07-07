import logging
from datetime import timedelta
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from .api_client import GoGreenEnergyApiClient
from .const import DEFAULT_PRODUCT_KEY, DEFAULT_OPTIONS

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    api_client = GoGreenEnergyApiClient()

    async def async_update_data():
        return await api_client.fetch_price_data(product_key=DEFAULT_PRODUCT_KEY, options=DEFAULT_OPTIONS)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,  # Pass the logger here
        name="GoGreenEnergy Price",
        update_method=async_update_data,
        update_interval=timedelta(hours=1),  # Update every hour
    )

    await coordinator.async_config_entry_first_refresh()
    sensor = GoGreenEnergySensor(coordinator)
    async_add_entities([sensor])

class GoGreenEnergySensor(CoordinatorEntity, Entity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._attr_name = "GoGreenEnergy Price"
        self._attr_unit_of_measurement = "EUR/kWh"  # Changed unit

    @property
    def state(self):
        price_cents = self.coordinator.data.get("price")
        if price_cents is not None:
            return round(price_cents / 100, 4)  # Convert to EUR, 4 decimals for kWh prices
        return None

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data
        return {
            "period": data.get("period"),
            "product": data.get("product"),
            "options": ", ".join(data.get("options", []))
        }


