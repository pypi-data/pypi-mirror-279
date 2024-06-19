from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer, WritableNestedSerializer
from ipam.api.serializers import NestedPrefixSerializer

from ..models import Processor, Endpoint, Stream, Format


# Format ---------------------------------------------------------------------------------------------------------------

class NestedFormatSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_multicast_stream_mapping-api:format-detail'
    )

    class Meta:
        model = Format
        fields = ('id', 'url', 'display', 'name')


class FormatSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_multicast_stream_mapping-api:format-detail'
    )

    class Meta:
        model = Format
        fields = (
            'id', 'url', 'display', 'name', 'type', 'res_h', 'res_w', 'fps', 'audio_ch', 'port', 'comments',
            'description', 'custom_fields', 'created', 'last_updated',
        )


# Processor ------------------------------------------------------------------------------------------------------------

class NestedProcessorSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_multicast_stream_mapping-api:processor-detail'
    )

    class Meta:
        model = Processor
        fields = ('id', 'url', 'display', 'name')


class ProcessorSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_multicast_stream_mapping-api:processor-detail'
    )

    class Meta:
        model = Processor
        fields = (
            'id', 'url', 'display', 'name', 'device', 'module', 'description',
            'comments', 'tags', 'custom_fields', 'created', 'last_updated',
        )


# Endpoint -------------------------------------------------------------------------------------------------------------

class NestedEndpointSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_multicast_stream_mapping-api:endpoint-detail'
    )

    class Meta:
        model = Endpoint
        fields = ('id', 'url', 'display', 'name')


class EndpointSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_multicast_stream_mapping-api:endpoint-detail'
    )

    class Meta:
        model = Endpoint
        fields = (
            'id', 'url', 'display', 'name', 'device', 'processor', 'interface', 'endpoint_type', 'primary_ip',
            'secondary_ip', 'max_bandwidth', 'supported_formats', 'switch_method', 'signal_type', 'comments',
            'description', 'tags', 'custom_fields', 'created', 'last_updated',
        )


# Stream ---------------------------------------------------------------------------------------------------------------

class NestedStreamSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_multicast_stream_mapping-api:stream-detail'
    )

    class Meta:
        model = Stream
        fields = ('id', 'url', 'display', 'name')


class StreamSerializer(NetBoxModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_multicast_stream_mapping-api:stream-detail'
    )

    class Meta:
        model = Stream
        fields = (
            'id', 'url', 'display', 'name', 'sender', 'receivers', 'bandwidth', 'formats', 'signal_type',
            'comments', 'description', 'tags', 'custom_fields', 'created', 'last_updated',
        )
