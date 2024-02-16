import json
from django.test import RequestFactory, TestCase, override_settings
from unittest.mock import Mock

from django.urls import reverse

from .views import CloudingAPIView, IsActiveView, UnarchiveView, StatusView
from .exceptions import CloudingAPIError


ERROR_JSON = {
    "type": "https://www.rfc-editor.org/rfc/rfc7231#section-6.6.1",
    "title": "Internal Server Error",
    "status": 500,
    "traceId": "00000000-0000-0000-0000-000000000000"
}


class TestCloudingAPIView(TestCase):
    """Only test the case where the server_id is provided in the request. Other cases are tested in the test_api_models.py file."""

    @override_settings(CLOUDING_API_KEY='test_key', CLOUDING_SERVER_ID='123')
    def test_get_server(self):
        request = RequestFactory().get('/', {'server_id': '456'})
        server = CloudingAPIView().get_server(request)
        self.assertEqual(server.server_id, '456')


class TestStatusView(TestCase):
    def setUp(self):
        self.request = RequestFactory().get(reverse('django_clouding_unarchive:server-status'))
        self.view = StatusView()
        self.view.get_server = Mock()
        self.view.get_server.return_value.get_status.return_value = 'active'
    
    def test_get(self):
        response = self.view.get(self.request)
        self.assertEqual(response.content, b'active')
    
    def test_get_error(self):
        self.view.get_server.return_value.get_status.side_effect = CloudingAPIError(ERROR_JSON)
        response = self.view.get(self.request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['status'], ERROR_JSON['status'])


class TestIsActiveView(TestCase):
    def setUp(self):
        self.request = RequestFactory().get(reverse('django_clouding_unarchive:server-is-active'))
        self.view = IsActiveView()
        self.view.get_server = Mock()
        self.view.get_server.return_value.is_active.return_value = True
    
    def test_get(self):
        response = self.view.get(self.request)
        self.assertEqual(response.content, b'active')
    
    def test_get_inactive(self):
        self.view.get_server.return_value.is_active.return_value = False
        response = self.view.get(self.request)
        self.assertEqual(response.content, b'inactive')
    
    def test_get_error(self):
        self.view.get_server.return_value.is_active.side_effect = CloudingAPIError(ERROR_JSON)
        response = self.view.get(self.request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['status'], ERROR_JSON['status'])
    

class TestUnarchiveView(TestCase):
    def setUp(self):
        self.request = RequestFactory().get(reverse('django_clouding_unarchive:unarchive-server'))
        self.view = UnarchiveView()
        self.view.get_server = Mock()
        self.view.get_server.return_value.unarchive.return_value = 'unarchived'
    
    def test_get(self):
        response = self.view.get(self.request)
        self.assertEqual(response.content, b'unarchived')

    def test_get_error(self):
        self.view.get_server.return_value.unarchive.side_effect = CloudingAPIError(ERROR_JSON)
        response = self.view.get(self.request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)['status'], ERROR_JSON['status'])