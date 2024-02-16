from django.test import TestCase, override_settings
from django.core.exceptions import ImproperlyConfigured
from unittest.mock import patch

from .api_models import CloudingAPI
from .exceptions import CloudingAPIError

class TestCloudingAPI(TestCase):
    def setUp(self):
        # Set up any necessary data or objects before running each test case
        pass

    @override_settings(CLOUDING_API_KEY=None, CLOUDING_SERVER_ID='123')
    def test_api_init_no_api_key(self):
        with self.assertRaises(ImproperlyConfigured) as context:
            CloudingAPI()
    
    @override_settings(CLOUDING_API_KEY='123', CLOUDING_SERVER_ID=None)
    def test_api_init_no_server_id(self):
        with self.assertRaises(ImproperlyConfigured) as context:
            CloudingAPI()
    
    @override_settings(CLOUDING_API_KEY='123', CLOUDING_SERVER_ID='123')
    def test_api_init(self):
        api = CloudingAPI()
        self.assertEqual(api.api_key, '123')
        self.assertEqual(api.server_id, '123')
    
    @override_settings(CLOUDING_API_KEY='123', CLOUDING_SERVER_ID='123')
    def test_api_init_params(self):
        api = CloudingAPI('456', '456')
        self.assertEqual(api.api_key, '456')
        self.assertEqual(api.server_id, '456')
    
    def test_get_status_invalid_api_key_or_server_id(self):
        api = CloudingAPI('123', '123')
        with self.assertRaises(CloudingAPIError) as context:
            api.get_status()
    
    @patch('requests.get')
    def test_get_status_error(self, mock_requests_get):
        mock_requests_get.return_value.ok = False
        mock_requests_get.return_value.json.return_value = {
            "type": "https://www.rfc-editor.org/rfc/rfc7231#section-6.6.1",
            "title": "Internal Server Error",
            "status": 500,
            "traceId": "00000000-0000-0000-0000-000000000000"
        }

        with self.assertRaises(CloudingAPIError) as context:
            api = CloudingAPI('123', '123')
            api.get_status()

    @patch('requests.get')
    def test_get_status(self, mock_requests_get):
        mock_requests_get.return_value.ok = True
        mock_requests_get.return_value.json.return_value = {'status': 'Archived'}
        api = CloudingAPI('123', '123')
        self.assertEqual(api.get_status(), 'Archived')
  
    @patch('requests.post')
    def test_unarchive_invalid_api_key_or_server_id(self, mock_requests_post):
        mock_requests_post.return_value.ok = False
        mock_requests_post.return_value.json.return_value = {
            "type": "https://www.rfc-editor.org/rfc/rfc7231#section-6.6.1",
            "title": "Internal Server Error",
            "status": 500,
            "traceId": "00000000-0000-0000-0000-000000000000"
        }
        api = CloudingAPI('123', '123')
        with self.assertRaises(CloudingAPIError) as context:
            api.unarchive()
    
    @patch('requests.post')
    def test_unarchive_error(self, mock_requests_post):
        mock_requests_post.return_value.ok = True
        mock_requests_post.return_value.json.return_value = {
            "status": "errored"
        }
        api = CloudingAPI('123', '123')
        with self.assertRaises(CloudingAPIError) as context:
            api.unarchive()
    
    @patch('requests.post')
    def test_unarchive(self, mock_requests_post):
        mock_requests_post.return_value.ok = True
        mock_requests_post.return_value.json.return_value = {
            "status": "completed"
        }
        api = CloudingAPI('123', '123')
        self.assertEqual(api.unarchive(), 'completed')
    
    @patch('requests.get')
    def test_is_active_active(self, mock_requests_get):
        mock_requests_get.return_value.ok = True
        mock_requests_get.return_value.json.return_value = {
            "status": "Active"
        }
        api = CloudingAPI('123', '123')
        self.assertTrue(api.is_active())

    @patch('requests.get')
    def test_is_active_archived(self, mock_requests_get):
        mock_requests_get.return_value.ok = True
        mock_requests_get.return_value.json.return_value = {
            "status": "Archived"
        }
        api = CloudingAPI('123', '123')
        self.assertFalse(api.is_active())
    
    @patch('requests.get')
    def test_is_active_error(self, mock_requests_get):
        mock_requests_get.return_value.ok = False
        mock_requests_get.return_value.json.return_value = {
            "status": "errored"
        }
        api = CloudingAPI('123', '123')
        with self.assertRaises(CloudingAPIError) as context:
            api.is_active()
    
    

         