from django.views.generic import FormView, TemplateView, RedirectView
from core.forms import PictureUploadForm
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest

import os
import shutil
from django.conf import settings


class AccessMixin(object):
    def dispatch(self, request, *args, **kwargs):
        # Checking perms
        return super(AccessMixin, self).dispatch(request, *args, **kwargs)


class AnonUploadView(FormView):
    template_name = 'core/upload.html'
    form_class = PictureUploadForm
    success_url = reverse_lazy('core:upload')

    def form_valid(self, form):
        picture = form.files.get('picture')
        with open(os.path.join(settings.UPLOAD_TO, picture.name), 'wb+') as dst:
            shutil.copyfileobj(
                picture.file,
                dst
            )
        return super(AnonUploadView, self).form_valid(form)


class DownloadView(AccessMixin, RedirectView):
    http_method_names = ['get']
    
    def dispatch(self, request, filename, *args, **kwargs):
        if filename is None:
            return HttpResponseBadRequest()
        self.url = os.path.join(settings.UPLOAD_URL, filename)
        return super(DownloadView, self).dispatch(request, *args, **kwargs)


class LinksView(AccessMixin, TemplateView):
    template_name = 'core/link_list.html'

    def dispatch(self, request, *args, **kwargs):
        # if not self.request.user.is_superuser:
        #     return HttpResponseForbidden()
        return super(LinksView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(LinksView, self).get_context_data(**kwargs)
        context['filenames'] = os.listdir(settings.UPLOAD_TO)
        return context
