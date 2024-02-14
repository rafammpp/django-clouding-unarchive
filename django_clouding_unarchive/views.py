from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .api_models import CloudingAPI
from .exceptions import CloudingAPIError


class CloudingAPIView(LoginRequiredMixin, View):

    def get_server(self, request):
        server_id = request.GET.get('server_id')
        return CloudingAPI(server_id)


class IsActiveView(CloudingAPIView):
    def get(self, request):
        server = self.get_server(request)
        try:
            if server.is_active():
                return HttpResponse('active')
            return HttpResponse('inactive')
        except CloudingAPIError as e:
            return HttpResponseBadRequest(str(e))
    

class UnarchiveView(CloudingAPIView):
    def get(self, request):
        server = self.get_server(request)
        try:
            return HttpResponse(server.unarchive())
        except CloudingAPIError as e:
            return HttpResponseBadRequest(str(e))


class StatusView(CloudingAPIView):
    def get(self, request):
        server = self.get_server(request)
        try:
            return HttpResponse(server.get_status())
        except CloudingAPIError as e:
            return HttpResponseBadRequest(str(e))
