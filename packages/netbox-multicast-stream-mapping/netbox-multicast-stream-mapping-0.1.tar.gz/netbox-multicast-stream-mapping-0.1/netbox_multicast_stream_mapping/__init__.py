from extras.plugins import PluginConfig


class NetBoxMulticastStreamMappingConfig(PluginConfig):
    name = 'netbox_multicast_stream_mapping'
    verbose_name = ' NetBox Multicast Stream Mapping'
    description = 'Enable multicast stream mapping from senders to receivers in netbox'
    version = '0.1'
    min_version = '3.4.0'
    base_url = 'stream-mapping' # TODO


config = NetBoxMulticastStreamMappingConfig
