import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from .exceptions import CloudingAPIError


class CloudingAPI:
    def __init__(self, api_key=None, server_id=None):
        self.api_key = api_key or settings.CLOUDING_API_KEY
        self.server_id = server_id or settings.CLOUDING_SERVER_ID
        
        if not self.api_key:
            raise ImproperlyConfigured("Missing CLOUDING_API_KEY in settings")
        if not self.server_id:
            raise ImproperlyConfigured("Missing CLOUDING_SERVER_ID")
    
    def get_status(self):
        """@return Enum: 
            'Creating' 'Starting' 'Active' 'Stopped' 'Stopping' 'Rebooting' 'Resize' 'Unarchiving' 'Archived' 'Archiving' 'Pending' 'ResettingPassword' 'RestoringBackup' 'RestoringSnapshot' 'Deleted' 'Deleting' 'Error' 'Unknown'
        """
        url = f"https://api.clouding.io/v1/servers/{self.server_id}"
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        response = requests.get(url, headers=headers)
        if response.ok:
            data = response.json()
            return data['status']
        else:
            raise CloudingAPIError(response.json())
    
    def unarchive(self):
        url = f"https://api.clouding.io/v1/servers/{self.server_id}/unarchive"
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        response = requests.post(url, headers=headers)
        if response.ok:
            data = response.json()
            if data['status'] == "errored": # posible status: "pending" "inProgress" "completed" "errored"
                raise CloudingAPIError(data)
            return data['status']
        else:
            raise CloudingAPIError(data)

    def is_creating(self):
        return self.get_status() == 'Creating'

    def is_starting(self):
        return self.get_status() == 'Starting'

    def is_active(self):
        return self.get_status() == 'Active'

    def is_stopped(self):
        return self.get_status() == 'Stopped'

    def is_stopping(self):
        return self.get_status() == 'Stopping'

    def is_rebooting(self):
        return self.get_status() == 'Rebooting'

    def is_resizing(self):
        return self.get_status() == 'Resize'

    def is_unarchiving(self):
        return self.get_status() == 'Unarchiving'

    def is_archived(self):
        return self.get_status() == 'Archived'

    def is_archiving(self):
        return self.get_status() == 'Archiving'

    def is_pending(self):
        return self.get_status() == 'Pending'

    def is_resetting_password(self):
        return self.get_status() == 'ResettingPassword'

    def is_restoring_backup(self):
        return self.get_status() == 'RestoringBackup'

    def is_restoring_snapshot(self):
        return self.get_status() == 'RestoringSnapshot'

    def is_deleted(self):
        return self.get_status() == 'Deleted'

    def is_deleting(self):
        return self.get_status() == 'Deleting'

    def is_error(self):
        return self.get_status() == 'Error'

    def is_unknown(self):
        return self.get_status() == 'Unknown'   
