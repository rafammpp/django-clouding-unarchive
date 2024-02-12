# Django Clouding Unarchive

## How to install
Install the app with pip.

In settings place this two vars:
```
# Clouding
CLOUDING_API_KEY = env('CLOUDING_API_KEY')
CLOUDING_SERVER_ID = env('CLOUDING_SERVER_ID')
```
And setup them properly in env variables

Update settings.py INSTALLED_APPS:
```
INSTALLED_APPS = [
    ...,
    "django_clouding_unarchive.apps.DjangoCloudingUnarchiveConfig",
    ...,
]
```

Update urls.py to point to the app urls:
```
urlpatterns = [
    path("clouding-api/", include("django_clouding_unarchive.urls")),
    ...,
]
```

Include this in any template inside the admin
```
{% include "django_clouding_unarchive/button.html" %}
```

