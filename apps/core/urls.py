from django.conf.urls import url

from apps.core.api import DealListAPIView, HubTokenAPIView
from apps.core.views import IndexView, ListDealView

urlpatterns = [
    url(r'^get-code/$', IndexView.as_view(), name='get_code'),
    url(r'^list-deals-api/$', DealListAPIView.as_view(), name='list_deals_api'),
    url(r'^get-token/$', HubTokenAPIView.as_view(), name='get_token'),
    url(r'^$', ListDealView.as_view(), name='index'),
]
