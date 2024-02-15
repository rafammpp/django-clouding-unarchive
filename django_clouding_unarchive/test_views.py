from django.test import RequestFactory, TestCase, override_settings
from django.core.exceptions import ImproperlyConfigured
from unittest.mock import Mock, patch

from .views import CloudingAPIView, IsActiveView, UnarchiveView, StatusView
from .exceptions import CloudingAPIError


class TestCloudingAPIView(TestCase):
    """Only test the case where the server_id is provided in the request. Other cases are tested in the test_api_models.py file."""

    @override_settings(CLOUDING_API_KEY='test_key', CLOUDING_SERVER_ID='123')
    def test_get_server(self):
        request = RequestFactory().get('/', {'server_id': '456'})
        print(request.GET)
        server = CloudingAPIView().get_server(request)
        self.assertEqual(server.server_id, '456')
    

class TestStatusView(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/status')
        self.view = StatusView()
        self.view.get_server = Mock()
        self.view.get_server.return_value.get_status.return_value = 'active'
    
    def test_get(self):
        response = self.view.get(self.request)
        self.assertEqual(response.content, b'active')
    
    def test_get_error(self):
        self.view.get_server.return_value.get_status.side_effect = CloudingAPIError('test error')
        response = self.view.get(self.request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'test error')


class TestIsActiveView(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/is_active')
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
        self.view.get_server.return_value.is_active.side_effect = CloudingAPIError('test error')
        response = self.view.get(self.request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'test error')
    

class TestUnarchiveView(TestCase):
    def setUp(self):
        self.request = RequestFactory().get('/unarchive')
        self.view = UnarchiveView()
        self.view.get_server = Mock()
        self.view.get_server.return_value.unarchive.return_value = 'unarchived'
    
    def test_get(self):
        response = self.view.get(self.request)
        self.assertEqual(response.content, b'unarchived')

    def test_get_error(self):
        self.view.get_server.return_value.unarchive.side_effect = CloudingAPIError('test error')
        response = self.view.get(self.request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b'test error')