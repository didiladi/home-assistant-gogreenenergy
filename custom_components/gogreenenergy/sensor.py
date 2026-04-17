import logging
from datetime import timedelta
import voluptuous as vol

import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from .api_client import GoGreenEnergyApiClient
from .const import DOMAIN, DEFAULT_PRODUCT_KEY, DEFAULT_OPTIONS, DEFAULT_ADDITIONAL_FEE

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional("product_key", default=DEFAULT_PRODUCT_KEY): cv.string,
    vol.Optional("options", default=list(DEFAULT_OPTIONS)): cv.ensure_list,
    vol.Optional("additional_fee_per_kwh", default=DEFAULT_ADDITIONAL_FEE): vol.Coerce(float),
})

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    api_client = GoGreenEnergyApiClient()
    product_key = config.get("product_key", DEFAULT_PRODUCT_KEY)
    options = tuple(config.get("options", DEFAULT_OPTIONS))
    additional_fee_per_kwh = config.get("additional_fee_per_kwh", DEFAULT_ADDITIONAL_FEE)

    async def async_update_data():
        return await api_client.fetch_price_data(product_key=product_key, options=options)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="GoGreenEnergy Price",
        update_method=async_update_data,
        update_interval=timedelta(hours=1),
    )

    await coordinator.async_config_entry_first_refresh()
    sensor = GoGreenEnergySensor(coordinator, additional_fee_per_kwh)
    async_add_entities([sensor])

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the GoGreenEnergy sensor from a config entry."""
    api_client = GoGreenEnergyApiClient()
    product_key = entry.data.get("product_key", DEFAULT_PRODUCT_KEY)
    
    # Process options from the UI boolean switches
    options = []
    if entry.data.get("option_plus", True):
        options.append("plus")
    if entry.data.get("option_future", False):
        options.append("future")
        
    additional_fee_per_kwh = entry.data.get("additional_fee_per_kwh", DEFAULT_ADDITIONAL_FEE)

    async def async_update_data():
        return await api_client.fetch_price_data(product_key=product_key, options=tuple(options))

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="GoGreenEnergy Price",
        update_method=async_update_data,
        update_interval=timedelta(hours=1),
    )

    await coordinator.async_config_entry_first_refresh()
    sensor = GoGreenEnergySensor(coordinator, additional_fee_per_kwh)
    async_add_entities([sensor])

class GoGreenEnergySensor(CoordinatorEntity, Entity):
    def __init__(self, coordinator, additional_fee_per_kwh):
        super().__init__(coordinator)
        self._attr_name = "GoGreenEnergy Price"
        self._attr_unit_of_measurement = "EUR/kWh"
        self._additional_fee = additional_fee_per_kwh

    @property
    def state(self):
        price_cents = self.coordinator.data.get("price")
        if price_cents is not None:
            base_price_eur = price_cents / 100
            return round(base_price_eur + self._additional_fee, 4)
        return None

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        data = self.coordinator.data
        if data and "product" in data:
            return f"{DOMAIN}_{data['product']}_{self._additional_fee}".replace(" ", "_").lower()
        return None

    @property
    def extra_state_attributes(self):
        data = self.coordinator.data
        return {
            "period": data.get("period"),
            "product": data.get("product"),
            "options": ", ".join(data.get("options", [])),
            "base_price_cents": data.get("price"),
            "additional_fee_per_kwh": self._additional_fee
        }
