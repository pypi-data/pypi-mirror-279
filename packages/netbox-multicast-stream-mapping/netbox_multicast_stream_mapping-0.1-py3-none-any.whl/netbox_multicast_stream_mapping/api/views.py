from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import *

# View Sets for api


class FormatViewSet(NetBoxModelViewSet):
    queryset = models.Format.objects.prefetch_related('tags')
    serializer_class = FormatSerializer
    filterset_class = filtersets.FormatFilterSet


class ProcessorViewSet(NetBoxModelViewSet):
    queryset = models.Processor.objects.prefetch_related('tags')
    serializer_class = ProcessorSerializer
    filterset_class = filtersets.ProcessorFilterSet


class EndpointViewSet(NetBoxModelViewSet):
    queryset = models.Endpoint.objects.prefetch_related('tags')
    serializer_class = EndpointSerializer
    filterset_class = filtersets.EndpointFilterSet


class StreamViewSet(NetBoxModelViewSet):
    queryset = models.Stream.objects.prefetch_related('tags')
    serializer_class = StreamSerializer
    filterset_class = filtersets.StreamFilterSet


