# Django Clouding Unarchive

## How to install
Install the app with pip.

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
The view requires the user to be authenticated. So 

You can also specify some vars to configure the button, all are optional:
- css_classes: string with the classes to apply to the button.
- server_id: the server id to unarchive. If not specified, it will use the CLOUDING_SERVER_ID from settings.
- on_success_url: the url to link after the unarchive process is done.
- test_on_success_url: "true" or "false". This will make an http request to also test the availability of the server. If the server is not available, it will wait until it is available and then show the link.
- label: the label of the button. Default is "Wake up the server".

Example:
```
{% include "django_clouding_unarchive/button.html" with css_classes="btn btn-primary" server_id=1234abc on_success_url="https://plausible.example.org" test_on_success_url="true" label="Wake up Plausible" %}
```

You can include multiple buttons in the same template, each with different configurations. Make sure the server_id is different in each button.




## My use case
I use Plausible Analytics to track my website. I have a small server in one provider that I only use to track the pageviews events. But for making queries and retrieve the data, like the number of pageviews for the last ten years, I need a way more powerful server. So I have a second server in clouding.io that I only use to make queries to the database and retrieve the data. To avoid the complete cost of having the server running 24/7, almost 300$/month, I made this app to unarchive the server only when I or the web editors need it. I only need to click a button in the django admin panel and the server will be ready in 40 seconds. When the server don't have any activity for 50 minutes, it will be archived again. This way I only pay some cents per hour when I need it.

So, if you have a team and need an expensive server only for some tasks, and you don't want to give access to the clouding.io panel to all the team, this app is for you.
