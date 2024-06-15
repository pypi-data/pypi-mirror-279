# gdmty_django_recaptcha_enterprise

**Library for Django that implements Google's reCaptcha Enterprise**

This library is a draft but it works. Was made because there is no library for Django that implements Google's reCaptcha Enterprise. But now this library provides a way to verify tokens from reCaptcha Enterprise.

Installation:

```bash
pip install gdmty-django-recaptcha-enterprise
```

Usage:

In settings.py:

```python
# import service_account from google.oauth2 and instanciate a Credentials object from your service account file 
from google.oauth2 import service_account

# put 'gdmty_django_recaptcha_enterprise' in INSTALLED_APPS
INSTALLED_APPS = [
    ...,
    'gdmty_django_recaptcha_enterprise',
    ...
]

# Set the following variables 
RECAPTCHA_ENTERPRISE_PROJECT_ID = 'your-project-id'

RECAPTCHA_ENTERPRISE_SITE_KEY_VERIFY = 'your-site-key' # This one is the site key for usage with seamless verification with the reCaptcha Enterprise API withouth user interaction
RECAPTCHA_ENTERPRISE_SITE_KEY_CHALLENGE = 'your-site-key' # This one is the site key for usage with challenge verification with the reCaptcha Enterprise API with user interaction
RECAPTCHA_ENTERPRISE_BYPASS_TOKEN = 'your-bypass-token' # Optional, only for debug and development usage. For production must be False. When DEBUG=False this must be False too or will not pass assesments never.

RECAPTCHA_CREDENTIALS_SERVICE_ACCOUNT = your-service-account
credentials = service_account.Credentials.from_service_account_info(RECAPTCHA_CREDENTIALS_SERVICE_ACCOUNT)
RECAPTCHA_ENTERPRISE_SERVICE_ACCOUNT_CREDENTIALS = credentials

# from_service_account_info() is a method from Credentials class that creates a Credentials object from a service account from a dictionary. You can use a json file with the service account info and load it with json.load to get the dictionary. or use from_service_account_file() method from Credentials class to load the json file and get the Credentials object directly.
```

In your code:

```python
# import assess_token from gdmty_django_recaptcha_enterprise.recaptcha, then you can use it to assess tokens where you need it. In this excample we show a hypothetical view that receives a token from a POST request.
# You can use the decorator requires_recaptcha to verify the token before the view is executed.

from gdmty_django_recaptcha_enterprise.recaptcha import RecaptchaEnterprise
from gdmty_django_recaptcha_enterprise.decorators import requires_recaptcha
from django.conf import settings


recaptcha = RecaptchaEnterprise(
    settings.RECAPTCHA_ENTERPRISE_PROJECT_ID, 
    settings.RECAPTCHA_ENTERPRISE_SITE_KEY_VERIFY, 
    settings.RECAPTCHA_ENTERPRISE_SERVICE_ACCOUNT_CREDENTIALS)

# each time you need to assess a token you can use the assess_token method from the recaptcha object, can be used from this decorator using the action parameter to assess.
# When the decorator is used, the decorator handles de request to get the token from the request and assess it, if the token is valid the view is executed, if not, the view is not executed and a 403 response is returned.
# 
@requires_recaptcha(action='action-to-verify')
def my_view(request):
    ...
    pass
    ...
```
