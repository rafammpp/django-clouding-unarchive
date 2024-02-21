import requests
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.views import View
from .api_models import CloudingAPI
from .exceptions import CloudingAPIError
from requests.exceptions import ConnectionError


class CloudingAPIView(LoginRequiredMixin, View):

    def get_server(self, request):
        server_id = request.GET.get('server_id')
        return CloudingAPI(server_id=server_id)


class IsActiveView(CloudingAPIView):
    def get(self, request):
        try:
            server = self.get_server(request)
        except ImproperlyConfigured as e:
            return HttpResponseBadRequest(str(e))
        try:
            if server.is_active():
                return HttpResponse('active')
            return HttpResponse('inactive')
        except CloudingAPIError as e:
            return HttpResponseBadRequest(str(e))


class UnarchiveView(CloudingAPIView):
    def get(self, request):
        try:
            server = self.get_server(request)
        except ImproperlyConfigured as e:
            return HttpResponseBadRequest(str(e))
        try:
            return HttpResponse(server.unarchive())
        except CloudingAPIError as e:
            return HttpResponseBadRequest(str(e))


class StatusView(CloudingAPIView):
    def get(self, request):
        try:
            server = self.get_server(request)
        except ImproperlyConfigured as e:
            return HttpResponseBadRequest(str(e))
        try:
            return HttpResponse(server.get_status())
        except CloudingAPIError as e:
            return HttpResponseBadRequest(str(e))


class ServerIsReadyView(CloudingAPIView):
    def get(self, request):
        url = request.GET.get('url')
        try:
            if not url:
                return HttpResponseBadRequest('url parameter is required')
            response = requests.head(url)
            return HttpResponse('ready' if response.ok else 'not ready')
        except ConnectionError:
            return HttpResponse('not ready')


class ServerNameView(CloudingAPIView):
    def get(self, request):
        try:
            server = self.get_server(request)
            return HttpResponse(server.name)
        except ImproperlyConfigured as e:
            return HttpResponseBadRequest(str(e))
        except CloudingAPIError as e:
            return HttpResponseBadRequest(str(e))
