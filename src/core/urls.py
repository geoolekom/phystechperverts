from django.conf.urls import url
from core.views import AnonUploadView, DownloadView, LinksView
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy

urlpatterns = [
    url(r'^$', RedirectView.as_view(url=reverse_lazy('core:pictures')), name='home'),
    url(r'upload/$', AnonUploadView.as_view(), name='upload'),
    url(r'download/(?P<filename>.+)/', DownloadView.as_view(), name='download'),
    url(r'pictures/', LinksView.as_view(), name='pictures')
]