from django.conf.urls import url
from .views import BarChart

urlpatterns = [
    url(r'^$', BarChart.as_view(), name = 'show_chart'),
]
