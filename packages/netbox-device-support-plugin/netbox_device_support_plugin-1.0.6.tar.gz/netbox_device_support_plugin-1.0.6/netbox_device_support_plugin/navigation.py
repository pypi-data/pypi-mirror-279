from django.conf import settings
from netbox.plugins import PluginMenuItem


# Get all needed settings from the plugin settings
PLUGIN_SETTINGS = settings.PLUGINS_CONFIG.get("netbox_device_support_plugin", dict())
DEVICE_VENDORS = PLUGIN_SETTINGS.get("DEVICE_VENDORS", ["Cisco"])
CISCO_MANUFACTURER = PLUGIN_SETTINGS.get("CISCO_MANUFACTURER", "Cisco")
FORTINET_MANUFACTURER = PLUGIN_SETTINGS.get("FORTINET_MANUFACTURER", "Fortinet")
PURESTORAGE_MANUFACTURER = PLUGIN_SETTINGS.get("PURESTORAGE_MANUFACTURER", "Pure Storage")

# Create an empty list to store the menu items
menu_items = []

#### Cisco Support ##########################################################################################

# Add the menu items for the Cisco device support views if configured in the plugin settings
if CISCO_MANUFACTURER in DEVICE_VENDORS:
    menu_items.append(
        PluginMenuItem(
            link="plugins:netbox_device_support_plugin:ciscodevicesupport_list",
            link_text="Cisco Device Support",
        )
    )
    menu_items.append(
        PluginMenuItem(
            link="plugins:netbox_device_support_plugin:ciscodevicetypesupport_list",
            link_text="Cisco Device Type Support",
        )
    )

#### Fortinet Support #######################################################################################

# Add the menu items for the Fortinet device support views if configured in the plugin settings
if FORTINET_MANUFACTURER in DEVICE_VENDORS:
    menu_items.append(
        PluginMenuItem(
            link="plugins:netbox_device_support_plugin:fortinetdevicesupport_list",
            link_text="Fortinet Device Support",
        )
    )

#### PureStorage Support ####################################################################################

# Add the menu items for the PureStorage device support views if configured in the plugin settings
if PURESTORAGE_MANUFACTURER in DEVICE_VENDORS:
    menu_items.append(
        PluginMenuItem(
            link="plugins:netbox_device_support_plugin:purestoragedevicesupport_list",
            link_text="PureStorage Device Support",
        )
    )

#### Menu Items #############################################################################################

# Convert the list of URL patterns to a tuple as the Django urlpatterns must be a tuple
menu_items = tuple(menu_items)
