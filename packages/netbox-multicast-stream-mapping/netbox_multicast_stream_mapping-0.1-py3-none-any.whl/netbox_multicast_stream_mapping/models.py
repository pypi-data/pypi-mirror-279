from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from utilities.choices import ChoiceSet
from netbox.models import NetBoxModel


# Choices --------------------------------------------------------------------------------------------------------------

# Choices for Endpoint Type -> Sender or Receiver?
class EndpointTypeChoices(ChoiceSet):
    key = 'Endpoint.endpoint_type'

    CHOICES = [
        ('sender', 'Sender', 'red'),
        ('receiver', 'Receiver', 'green'),
    ]


# Choices for Signal Type of Endpoint
class SignalTypeChoices(ChoiceSet):
    key = 'Endpoint.signal_type'

    CHOICES = [
        ('video', 'Video', 'blue'),
        ('audio', 'Audio', 'yellow'),
        ('metadata', 'Metadata', 'orange'),
    ]


# Choices for switch method (ST 2022-7)
class SwitchMethodChoices(ChoiceSet):
    key = 'Endpoint.switch_method'

    CHOICES = [
        ('sips_merge', 'SiPs Merge', 'cyan'),
        ('sips_split', 'SiPs Split', 'purple'),
    ]


# Choices for Signal Type of Format Preset
class FormatTypeChoices(ChoiceSet):
    key = 'Format.type'

    CHOICES = [
        ('video', 'Video', 'blue'),
        ('audio', 'Audio', 'yellow'),
        ('metadata', 'Metadata', 'orange'),
        ('ect', 'Ect.'),
    ]


# todo feste auswahloptionen fpr pixel, bandbreite, usw....
# choices for frame rates in Format Presets
class FpsChoices(ChoiceSet):
    key = 'Format.fps'

    CHOICES = [
        # progressive broadcast
        ('p25', 'p25'),
        ('p29.97', 'p29.97'),
        ('p30', 'p30'),
        ('p50', 'p50'),
        ('p59.94', 'p59.94'),
        ('p60', 'p60'),

        # interlaced broadcast
        ('i50', 'i50'),
        ('i59.94', 'i59.94'),
        ('i60', 'i60'),

        # high frame rate
        ('p100', 'p100'),
        ('p120', 'p120'),
        ('p144', 'p144'),
        ('p180', 'p180'),
        ('p240', 'p240'),
    ]


# Models ---------------------------------------------------------------------------------------------------------------

# model format presets -> are supported for endpoints
class Format(NetBoxModel):
    name = models.CharField(max_length=100)
    type = models.CharField(choices=FormatTypeChoices, null=True, blank=True)
    res_h = models.PositiveIntegerField(null=True, blank=True)
    res_w = models.PositiveIntegerField(null=True, blank=True)
    fps = models.CharField(choices=FpsChoices, null=True, blank=True)
    audio_ch = models.PositiveIntegerField(null=True, blank=True)
    port = models.PositiveIntegerField(null=True, blank=True) # todo min/max?
    comments = models.TextField(blank=True)
    description = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ("name",)
        unique_together = ("name",)

    # returns human readable name
    def __str__(self):
        return self.name

    # django convention for URL mapping
    def get_absolute_url(self):
        return reverse('plugins:netbox_multicast_stream_mapping:format', args=[self.pk])

    # returns badge color for multiple choice fields
    def get_type_color(self):
        return FormatTypeChoices.colors.get(self.type)


# model for internal processing units of devices -> has senders and receivers
class Processor(NetBoxModel): # todo device spalte anzahl an enpoints oder procs?
    name = models.CharField(max_length=100) # todo in tabellenansicht aus gerät auch device namen anzeigen?
    device = models.ForeignKey(to='dcim.Device', on_delete=models.CASCADE, related_name='+') # todo related_name='+' um keine beziehung rückwärst zu erstellen
    module = models.ForeignKey(to='dcim.Module', on_delete=models.CASCADE, related_name='+', null=True, blank=True) # todo logik -> modul muss zu device gehören
    description = models.CharField(max_length=500, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ("name",)
        unique_together = ("name",)
        # TODO mehr?

    # returns human readable name
    def __str__(self):
        return self.name

    # django convention for URL mapping
    def get_absolute_url(self):
        return reverse('plugins:netbox_multicast_stream_mapping:processor', args=[self.pk])

    # function to get number of endpoints for detail view template
    def get_endpoint_count(self):
        return self.endpoint_set.count()


# model for internal processing units of devices -> has senders and receivers
class Endpoint(NetBoxModel):
    name = models.CharField(max_length=100)
    device = models.ForeignKey(to='dcim.Device', on_delete=models.CASCADE, null=True, related_name='+') # todo related_name='+' um keine beziehung rückwärst zu erstellen
    processor = models.ForeignKey(to=Processor, on_delete=models.CASCADE)
    interface = models.ForeignKey(to='dcim.Interface', on_delete=models.SET_NULL, related_name='+', blank=True, null=True) # todo gleiche ip mehrfach! oder range?
    endpoint_type = models.CharField(choices=EndpointTypeChoices, null=True) # todo farben als plakette
    primary_ip = models.OneToOneField(to='ipam.IPAddress', on_delete=models.SET_NULL, related_name='+', blank=True, null=True) # todo gleiche ip mehrfach! oder range?
    secondary_ip = models.OneToOneField(to='ipam.IPAddress', on_delete=models.SET_NULL, related_name='+', blank=True, null=True)
    max_bandwidth = models.FloatField(null=True, blank=True)
    supported_formats = models.ManyToManyField(to=Format, blank=True) # todo filter basiert auf signal type?
    switch_method = models.CharField(choices=SwitchMethodChoices, null=True, blank=True) # todo plakette
    signal_type = models.CharField(choices=SignalTypeChoices, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ("name",)
        unique_together = ("name",)
        # todo mehr ?

    # returns human readable name
    def __str__(self):
        return self.name

    # django convention for URL mapping
    def get_absolute_url(self):
        return reverse('plugins:netbox_multicast_stream_mapping:endpoint', args=[self.pk])

    # returns badge color for multiple choice fields
    def get_signal_type_color(self):
        return SignalTypeChoices.colors.get(self.signal_type)

    # returns badge color for multiple choice fields
    def get_switch_method_color(self):
        return SwitchMethodChoices.colors.get(self.switch_method)

    # returns badge color for multiple choice fields
    def get_endpoint_type_color(self):
        return EndpointTypeChoices.colors.get(self.endpoint_type)


# model for internal processing units of devices -> has senders and receivers
class Stream(NetBoxModel):
    name = models.CharField(max_length=100)
    sender = models.ForeignKey(to=Endpoint, on_delete=models.CASCADE, related_name="sent_streams")
    receivers = models.ManyToManyField(to=Endpoint, related_name="received_streams")
    bandwidth = models.FloatField(null=True, blank=True)
    signal_type = models.CharField(choices=SignalTypeChoices, null=True, blank=True)
    protocol = models.CharField(max_length=100, blank=True)  # todo choice -> welche?
    formats = models.ManyToManyField(to=Format, blank=True)
    comments = models.TextField(blank=True)
    description = models.CharField(max_length=500, blank=True)

    class Meta:
        ordering = ("name",)
        unique_together = ("name",)

    # returns human readable name
    def __str__(self):
        return self.name

    # django convention for URL mapping
    def get_absolute_url(self):
        return reverse('plugins:netbox_multicast_stream_mapping:stream', args=[self.pk])

    # returns badge color for multiple choice fields
    def get_signal_type_color(self):
        return SignalTypeChoices.colors.get(self.signal_type)
