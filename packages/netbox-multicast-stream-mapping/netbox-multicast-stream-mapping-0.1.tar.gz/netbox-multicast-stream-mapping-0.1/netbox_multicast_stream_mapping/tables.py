import django_tables2 as tables
from django_tables2.utils import A
from netbox.tables import NetBoxTable, ChoiceFieldColumn, TagColumn, ManyToManyColumn, columns
from .models import *
# TODO spalte mit letzter änderung?


# table class for format tags
class FormatTable(NetBoxTable):
    name = tables.Column(linkify=True)
    type = ChoiceFieldColumn()
    res_h = tables.Column(verbose_name='Vertical Resolution')
    res_w = tables.Column(verbose_name='Horizontal Resolution')
    fps = ChoiceFieldColumn(verbose_name='Frame Rate')
    audio_ch = tables.Column(verbose_name='Number of Audio Channels')
    port = tables.Column(verbose_name='Network Port')
    comments = tables.Column()
    description = tables.Column()
    tags = TagColumn(url_name='plugins:netbox_multicast_stream_mapping:format_list')

    class Meta(NetBoxTable.Meta):
        model = Format
        fields = (
            'pk', 'id', 'name', 'type', 'res_h', 'res_w', 'fps', 'audio_ch', 'port', 'comments', 'description', 'tags'
        )
        default_columns = ('name', 'type', 'res_h', 'res_w', 'fps', 'audio_ch', 'port', 'description', 'tags')


# tabel class for processor
class ProcessorTable(NetBoxTable):
    name = tables.Column(linkify=True)
    device = tables.Column(linkify=True)
    module = tables.Column(linkify=True)
    endpoint_count = tables.LinkColumn(  # special column with link to child view of all endpoints of processor
        'plugins:netbox_multicast_stream_mapping:endpoint_children',  # URL of view
        args=[A("pk")],  # primary key as argument for filtering children
        verbose_name='Number of Endpoints')
    description = tables.Column()
    comments = tables.Column()
    tags = TagColumn(url_name='plugins:netbox_multicast_stream_mapping:processor_list')

    class Meta(NetBoxTable.Meta):
        model = Processor
        # template_name = 'utilities/tables/netbox_table.html'
        fields = ('pk', 'id', 'name', 'device', 'module', 'endpoint_count', 'description', 'comments', 'tags')
        default_columns = ('name', 'device', 'endpoint_count', 'tags', 'description')


# tabel class for endpoints
class EndpointTable(NetBoxTable):
    name = tables.Column(linkify=True)
    device = tables.Column(linkify=True)
    processor = tables.Column(linkify=True)
    interface = tables.Column(linkify=True)
    endpoint_type = ChoiceFieldColumn(verbose_name='Endpoint Type')
    primary_ip = tables.Column(linkify=True, verbose_name='Primary IP Address')
    secondary_ip = tables.Column(linkify=True, verbose_name='Secondary IP Address')
    max_bandwidth = tables.Column(verbose_name='Max. Bandwidth (Mbps)')
    supported_formats = ManyToManyColumn(verbose_name='Supported Formats', linkify=True)
    switch_method = ChoiceFieldColumn(verbose_name='Switch Method (2022-7)')
    signal_type = ChoiceFieldColumn(verbose_name='Signal Type')
    description = tables.Column()
    comments = tables.Column()
    tags = TagColumn(url_name='plugins:netbox_multicast_stream_mapping:endpoint_list')

    class Meta(NetBoxTable.Meta):
        model = Endpoint
        # template_name = 'utilities/tables/netbox_table.html'
        fields = (
            'pk', 'id', 'name', 'processor', 'interface', 'endpoint_type', 'primary_ip', 'secondary_ip',
            'max_bandwidth', 'supported_formats',  'signal_type', 'comments', 'description', 'tags'
        )
        default_columns = (
            'name', 'endpoint_type', 'signal_type', 'description',  'device', 'processor', 'switch_method',
            'supported_formats', 'primary_ip', 'secondary_ip', 'tags'
        )


# tabel class for streams
class StreamTable(NetBoxTable):
    name = tables.Column(linkify=True)
    sender = tables.Column(linkify=True)
    receivers = ManyToManyColumn(linkify=True) # todo ändern
    bandwidth = tables.Column()
    signal_type = ChoiceFieldColumn(verbose_name='Signal Type')
    protocol = tables.Column()
    formats = ManyToManyColumn(verbose_name='Supported Formats', linkify=True)
    comments = tables.Column()
    description = tables.Column()
    tags = TagColumn(url_name='plugins:netbox_multicast_stream_mapping:stream_list')

    class Meta(NetBoxTable.Meta):
        model = Stream
        # template_name = 'utilities/tables/netbox_table.html'
        fields = (
            'pk', 'id', 'name', 'sender', 'receivers', 'bandwidth', 'signal_type', 'protocol', 'formats', 'comments',
            'description', 'tags'
        )
        default_columns = ('name', 'signal_type', 'sender', 'receivers', 'description', 'tags')
