import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, DEFAULT_PRODUCT_KEY, DEFAULT_OPTIONS, DEFAULT_ADDITIONAL_FEE

class GoGreenEnergyConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for GoGreenEnergy."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # We can perform validation here if needed, but for now we just accept
            return self.async_create_entry(title=f"GoGreenEnergy ({user_input['product_key']})", data=user_input)

        data_schema = vol.Schema(
            {
                vol.Required("product_key", default=DEFAULT_PRODUCT_KEY): str,
                # For options, a simple boolean for 'plus' and 'future' is easiest for the UI
                vol.Optional("option_plus", default=True): bool,
                vol.Optional("option_future", default=False): bool,
                vol.Optional("additional_fee_per_kwh", default=DEFAULT_ADDITIONAL_FEE): vol.Coerce(float),
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
