from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .api_models import CloudingAPI
from .exceptions import CloudingAPIError


class CloudingAPIView(LoginRequiredMixin, View):
    server = CloudingAPI()


class IsActiveView(CloudingAPIView):
    def get(self, request):
        try:
            if self.server.is_active():
                return HttpResponse('active')
            return HttpResponse('inactive')
        except CloudingAPIError as e:
            return HttpResponseBadRequest(str(e))
    

class UnarchiveView(CloudingAPIView):
    def get(self, request):
        try:
            return HttpResponse(self.server.unarchive())
        except CloudingAPIError as e:
            return HttpResponseBadRequest(str(e))


class StatusView(CloudingAPIView):
    def get(self, request):
        try:
            return HttpResponse(self.server.get_status())
        except CloudingAPIError as e:
            return HttpResponseBadRequest(str(e))
