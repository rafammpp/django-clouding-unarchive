# Django Clouding Unarchive
This app allows you to unarchive a server in clouding.io with a single click in the Django admin panel. It is particularly useful for teams that require an expensive server occasionally but do not want to grant access to the clouding.io panel to all team members.


## How to install
Install the app with pip. For now, it is not available in PyPi, so you need to install it from the git repository:
```
pip install git+https://github.com/rafammpp/django-clouding-unarchive/
```

In settings place this two vars:
```
# Clouding
CLOUDING_API_KEY = env('CLOUDING_API_KEY')
CLOUDING_SERVER_ID = env('CLOUDING_SERVER_ID') # Optional if you specify it in the button
```
And setup them properly in env variables

Update settings.py INSTALLED_APPS:
```
INSTALLED_APPS = [
    ...
    "django_clouding_unarchive.apps.DjangoCloudingUnarchiveConfig",
    ...
]
```

Update urls.py to point to the app urls:
```
urlpatterns = [
    path("clouding-api/", include("django_clouding_unarchive.urls")),
    ...
]
```

Include this in any template to show the button:
```
{% include "django_clouding_unarchive/button.html" %}
```
All views from this app requires the user to be authenticated. 

You can also specify some vars to configure the button, all are optional:
- css_classes: string with the css classes to apply to the button.
- server_id: the server id to unarchive. If not specified, it will use the CLOUDING_SERVER_ID from settings.
- server_name: the server name to show in the button. If not specified, it will use the name setup in clouding.io
- on_success_url: the url to link after the unarchive process is done.
- test_on_success_url: True or False. This will make an http request to also test the availability of the server. If the server is not available, it will wait until it is available and then show the link.
- label: the label of the button. Default is "Wake up the server".
- friendly_messages: True or False. If true, it will show more human friendly messages, like "The server is waking up" instead of "The server is unarchiving".

Example:
```
{% include "django_clouding_unarchive/button.html" with css_classes="btn btn-primary" server_id=1234abc on_success_url="https://plausible.example.org" test_on_success_url=True label="Wake up Plausible" %}
```

You can include multiple buttons in the same template, each with different configurations. Make sure the server_id is different in each button.




## My use case
I use Plausible Analytics to track my website. I have a small server in one provider that I only use to track the pageview events. However, for querying and retrieving data, such as the number of pageviews for the last ten years, I require a more powerful server. To avoid the high cost of running the server 24/7 (approximately $300/month), I developed this Django Clouding Unarchive app. It allows me to unarchive the server with a single click in the Django admin panel, making it ready for use in just 40 seconds. When the server remains inactive for 50 minutes, it is automatically archived again, resulting in a cost of only a few cents per hour when needed. This app is particularly useful for teams that require an expensive server occasionally but do not want to grant access to the clouding.io panel to all team members.
