from django.conf.urls import url, include
from rest_framework import routers
from api import views



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
from api.views import LoginViewSet
router = routers.DefaultRouter()
router.register(r'task', LoginViewSet)
urlpatterns = [
        url(r'^login/$', include(router.urls)),
        # # url(r'auth',include('rest_framework.urls'))
        # url(r'^api/login$',LoginViewSet.as_view())
        ]