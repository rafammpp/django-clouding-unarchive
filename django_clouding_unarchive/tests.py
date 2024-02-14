from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from .views import IsActiveView, UnarchiveView, StatusView
from .api_models import CloudingAPI
from unittest.mock import patch

class ViewTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test', email='test@test.com', password='test')

    @patch.object(CloudingAPI, 'is_active')
    def test_IsActiveView(self, mock_is_active):
        mock_is_active.return_value = True
        request = self.factory.get('/is_active?server_id=1')
        request.user = self.user
        response = IsActiveView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'active')

    @patch.object(CloudingAPI, 'unarchive')
    def test_UnarchiveView(self, mock_unarchive):
        mock_unarchive.return_value = 'unarchived'
        request = self.factory.get('/unarchive?server_id=1')
        request.user = self.user
        response = UnarchiveView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'unarchived')

    @patch.object(CloudingAPI, 'get_status')
    def test_StatusView(self, mock_get_status):
        mock_get_status.return_value = 'status'
        request = self.factory.get('/status?server_id=1')
        self.user = self.user
        response = StatusView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'status')