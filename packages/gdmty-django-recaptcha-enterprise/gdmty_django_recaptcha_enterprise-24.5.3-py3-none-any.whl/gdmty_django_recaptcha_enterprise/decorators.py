from django.conf import settings
from functools import wraps
from .recaptcha import RecaptchaEnterprise
from django.http import HttpResponseBadRequest, HttpResponseForbidden

if settings.RECAPTCHA_ENTERPRISE_SERVICE_ACCOUNT_CREDENTIALS:

    recaptcha = RecaptchaEnterprise(
        settings.RECAPTCHA_ENTERPRISE_PROJECT_ID,
        settings.RECAPTCHA_ENTERPRISE_SITE_KEY_VERIFY,
        settings.RECAPTCHA_ENTERPRISE_SERVICE_ACCOUNT_CREDENTIALS)

    def requires_recaptcha_token(action=None):
        def decorator(view_func):
            @wraps(view_func)
            def _wrapped_view(request, *args, **kwargs):

                recaptcha_token = request.data.get('recaptcha_token')

                if not recaptcha_token:
                    return HttpResponseBadRequest("Falta el token de recaptcha")

                if not recaptcha.assess_token(recaptcha_token, action):
                    return HttpResponseForbidden("Petición inválida")

                return view_func(request, *args, **kwargs)

            return _wrapped_view

        return decorator
