from django.db.models import Count
from utilities.views import ViewTab, register_model_view
from netbox.views import generic

from .models import *
from .tables import *
from .filtersets import *
from .forms import *
from dcim.models import Device
# todo logik!" auswahl, filterung, ...

# Format ---------------------------------------------------------------------------------------------------------------


# detail view
class FormatView(generic.ObjectView):
    queryset = Format.objects.all()


# list view
class FormatListView(generic.ObjectListView):
    queryset = Format.objects.all()
    table = FormatTable
    filterset = FormatFilterSet
    filterset_form = FormatFilterForm


# edit view
class FormatEditView(generic.ObjectEditView):
    queryset = Format.objects.all()
    form = FormatForm

# bulk edit view
class FormatBulkEditView(generic.BulkEditView):
    queryset = Format.objects.all()
    filterset = FormatFilterSet
    table = FormatTable
    form = FormatBulkEditForm


# delete view
class FormatDeleteView(generic.ObjectDeleteView):
    queryset = Format.objects.all()


# bulk delete view
class FormatBulkDeleteView(generic.BulkDeleteView):
    queryset = Format.objects.prefetch_related("tags")
    filterset = FormatFilterSet
    table = FormatTable


# Processor ------------------------------------------------------------------------------------------------------------


# detail view
class ProcessorView(generic.ObjectView):
    queryset = Processor.objects.all()

    # extra function to get number of endpoints -> will be displayed in detail view -> template.html
    def get_extra_context(self, request, instance):
        endpoints = instance.endpoint_set.all()
        table = EndpointTable(endpoints)
        table.configure(request)

        return {'endpoints_table': table, }


# list view
class ProcessorListView(generic.ObjectListView):
    # annotate queryset to display count of endpoints in list view
    queryset = Processor.objects.annotate(endpoint_count=Count('endpoint'))
    table = ProcessorTable
    filterset = ProcessorFilterSet
    filterset_form = ProcessorFilterForm


# edit view
class ProcessorEditView(generic.ObjectEditView):
    queryset = Processor.objects.all()
    form = ProcessorForm


# bulk edit view
class ProcessorBulkEditView(generic.BulkEditView):
    queryset = Processor.objects.all()
    filterset = ProcessorFilterSet
    table = ProcessorTable
    form = ProcessorBulkEditForm


# delete view
class ProcessorDeleteView(generic.ObjectDeleteView):
    queryset = Processor.objects.all()


# bulk delete view
class ProcessorBulkDeleteView(generic.BulkDeleteView):
    # annotate queryset to display count of endpoints in list view
    queryset = Processor.objects.prefetch_related("tags").annotate(endpoint_count=Count('endpoint'))
    filterset = ProcessorFilterSet
    table = ProcessorTable


# Endpoint -------------------------------------------------------------------------------------------------------------


# detail view
class EndpointView(generic.ObjectView):
    queryset = Endpoint.objects.all()


# list view
class EndpointListView(generic.ObjectListView):
    queryset = Endpoint.objects.all()
    table = EndpointTable
    filterset = EndpointFilterSet
    filterset_form = EndpointFilterForm


# edit view
class EndpointEditView(generic.ObjectEditView):
    queryset = Endpoint.objects.all()
    form = EndpointForm


# bulk edit view
class EndpointBulkEditView(generic.BulkEditView):
    queryset = Endpoint.objects.all()
    filterset = EndpointFilterSet
    table = EndpointTable
    form = EndpointBulkEditForm


# delete view
class EndpointDeleteView(generic.ObjectDeleteView):
    queryset = Endpoint.objects.all()


# bulk delete view
class EndpointBulkDeleteView(generic.BulkDeleteView):
    queryset = Endpoint.objects.prefetch_related("tags")
    filterset = EndpointFilterSet
    table = EndpointTable


# Stream ---------------------------------------------------------------------------------------------------------------


# detail view
class StreamView(generic.ObjectView):
    queryset = Stream.objects.all()


# list view
class StreamListView(generic.ObjectListView):
    queryset = Stream.objects.all()
    table = StreamTable
    filterset = StreamFilterSet
    filterset_form = StreamFilterForm


# edit view
class StreamEditView(generic.ObjectEditView):
    queryset = Stream.objects.all()
    form = StreamForm


# bulk edit view
class StreamBulkEditView(generic.BulkEditView):
    queryset = Stream.objects.all()
    filterset = StreamFilterSet
    table = StreamTable
    form = StreamBulkEditForm


# delete view
class StreamDeleteView(generic.ObjectDeleteView):
    queryset = Stream.objects.all()


# bulk delete view
class StreamBulkDeleteView(generic.BulkDeleteView):
    queryset = Stream.objects.prefetch_related("tags")
    filterset = StreamFilterSet
    table = StreamTable


# Other ----------------------------------------------------------------------------------------------------------------


# todo spalte in device list view?
# todo überschrift anpassen? in tempalte!!
# processor view for devices -> shows all processors of selected device
@register_model_view(model=Device, name='Processors', path='processors')
class DeviceProcessorView(generic.ObjectChildrenView):
    queryset = Device.objects.all()
    child_model = Processor
    table = ProcessorTable
    filterset = ProcessorFilterSet
    template_name = 'netbox_multicast_stream_mapping/processor_list.html'

    # creates tab in device detail view showing all linked processors
    tab = ViewTab(
        label="Processors",  # display name
        weight=100,  # weight for order in tab row
        badge=lambda obj: Processor.objects.filter(device=obj).count(),  # badge with number of linked processors
    )

    # returns all children processors and also annotates queryset with number of endpoints to display in list view
    def get_children(self, request, instance):
        return Processor.objects.filter(device=instance).annotate(endpoint_count=Count('endpoint'))


# todo spalte in device list view?
# processor view for devices
@register_model_view(model=Device, name='Endpoints', path='endpoints')
class DeviceEndpointView(generic.ObjectChildrenView):
    queryset = Device.objects.all()
    child_model = Endpoint
    table = EndpointTable
    filterset = EndpointFilterSet
    template_name = 'netbox_multicast_stream_mapping/processor_list.html'

    # creates tab in device detail view showing all linked endpoints
    tab = ViewTab(
        label="Endpoints",  # display name
        weight=110,  # weight for order in tab row -> one after processor tab
        badge=lambda obj: Endpoint.objects.filter(device=obj).count(),  # badge with number of linked endpoints
    )

    # returns all children endpoints of current device
    def get_children(self, request, instance):
        return Endpoint.objects.filter(device=instance)


# endpoint view for single processor -> shows all linked endpoints
class EndpointChildView(generic.ObjectChildrenView):
    queryset = Processor.objects.all().prefetch_related('endpoint_set')
    child_model = Endpoint
    table = EndpointTable
    template_name = "netbox_multicast_stream_mapping/endpoint_list.html"

    # returns all children endpoints of current processor
    def get_children(self, request, parent):
        return parent.endpoint_set.all()
