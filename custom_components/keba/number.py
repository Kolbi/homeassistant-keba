"""Number entities for keba."""

from keba_kecontact.connection import KebaKeContact
from keba_kecontact.wallbox import Wallbox

from homeassistant.components.number import NumberEntity, NumberEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, ELECTRIC_CURRENT_AMPERE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import KebaBaseEntity
from .const import DOMAIN, KEBA_CONNECTION


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Keba charging station number from config entry."""
    keba: KebaKeContact = hass.data[DOMAIN][KEBA_CONNECTION]
    entities: list[KebaNumber] = []

    wallbox = keba.get_wallbox(config_entry.data[CONF_HOST])
    number_description = NumberEntityDescription(
        key="Curr user",
        name="Charging current",
        native_unit_of_measurement=ELECTRIC_CURRENT_AMPERE,
        native_min_value=6,  # technical minimum
        native_max_value=63,  # technical maximum
        native_step=1,  # tehcnically possible step
    )
    entities.extend([KebaNumber(wallbox, number_description)])
    async_add_entities(entities, True)


class KebaNumber(KebaBaseEntity, NumberEntity):
    """Representation of a keba Number entity."""

    def __init__(
        self,
        wallbox: Wallbox,
        description: NumberEntityDescription,
    ) -> None:
        """Initialize the number entity."""
        super().__init__(wallbox, description)

    async def async_update(self):
        """Update the number with latest cached states from the device."""
        self._attr_native_max_value = self._wallbox.get_value("Curr HW")
        self._attr_native_value = self._wallbox.get_value(self.entity_description.key)

    async def async_set_native_value(self, value: float) -> None:
        """Set a new value."""
        await self._wallbox.set_current(value)
