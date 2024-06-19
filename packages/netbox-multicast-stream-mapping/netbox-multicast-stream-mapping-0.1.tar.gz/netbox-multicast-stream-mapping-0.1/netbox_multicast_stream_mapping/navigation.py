from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices
# todo version 4.0?

# Buttons --------------------------------------------------------------------------------------------------------------

processor_buttons = [
    PluginMenuButton(
        link='plugins:netbox_multicast_stream_mapping:processor_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN
    )
]


endpoint_button = [
    PluginMenuButton(
        link='plugins:netbox_multicast_stream_mapping:endpoint_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN
    )
]


stream_button = [
    PluginMenuButton(
        link='plugins:netbox_multicast_stream_mapping:stream_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN
    )
]


format_button = [
    PluginMenuButton(
        link='plugins:netbox_multicast_stream_mapping:format_add',
        title='Add',
        icon_class='mdi mdi-plus-thick',
        color=ButtonColorChoices.GREEN
    )
]


# Menu Items -----------------------------------------------------------------------------------------------------------

menu_items = (
    PluginMenuItem(
        link='plugins:netbox_multicast_stream_mapping:processor_list',
        link_text='Processors',
        buttons=processor_buttons
    ),

    PluginMenuItem(
        link='plugins:netbox_multicast_stream_mapping:endpoint_list',
        link_text='Endpoints',
        buttons=endpoint_button
    ),

    PluginMenuItem(
        link='plugins:netbox_multicast_stream_mapping:stream_list',
        link_text='Streams',
        buttons=stream_button
    ),

    PluginMenuItem(
        link='plugins:netbox_multicast_stream_mapping:format_list',
        link_text='Format Tags',
        buttons=format_button
    ),
)
