from netbox.search import SearchIndex, register_search
from .models import *


@register_search
class FormatIndex(SearchIndex):
    model = Format
    fields = (
        ('name', 100),
        ('type', 100),
        ('res_h', 100),
        ('description', 500),
        ('comments', 5000),
    )


@register_search
class ProcessorIndex(SearchIndex):
    model = Processor
    fields = (
        ('name', 100),
        ('device', 100),
        ('module', 100),
        ('description', 500),
        ('comments', 5000),
    )


@register_search
class EndpointIndex(SearchIndex):
    model = Endpoint
    fields = (
        ('name', 100),
        ('device', 100),
        ('processor', 100),
        ('endpoint_type', 100),
        ('switch_method', 100),
        ('signal_type', 100),
        ('description', 500),
        ('comments', 5000),
    )


@register_search
class StreamIndex(SearchIndex):
    model = Stream
    fields = (
        ('name', 100),
        ('sender', 100),
        ('receivers', 100),
        ('signal_type', 100),
        ('protocol', 100),
        ('formats', 100),
        ('description', 500),
        ('comments', 5000),
    )
