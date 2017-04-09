from django.views.generic import FormView, TemplateView, RedirectView
from core.forms import PictureUploadForm
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.utils import timezone

import hashlib
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
        print(picture.size)
        if picture.size > 10*1024*1024:
            return HttpResponseForbidden()
        new_filename = '{0}-{1}.{2}'.format(
            timezone.now().timestamp(),
            hashlib.md5(picture.name.encode()).hexdigest(),
            picture.name.split('.')[-1]
        )
        with open(os.path.join(settings.UPLOAD_TO, new_filename), 'wb+') as dst:
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
        context['filenames'] = reversed(os.listdir(settings.UPLOAD_TO))
        return context
