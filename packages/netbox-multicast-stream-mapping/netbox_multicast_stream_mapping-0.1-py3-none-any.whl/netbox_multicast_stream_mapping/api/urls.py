from netbox.api.routers import NetBoxRouter
from . import views

# url router for api


app_name = 'netbox_multicast_stream_mapping'

router = NetBoxRouter()

router.register('formats', views.FormatViewSet)
router.register('processors', views.ProcessorViewSet)
router.register('endpoints', views.EndpointViewSet)
router.register('streams', views.StreamViewSet)


urlpatterns = router.urls
