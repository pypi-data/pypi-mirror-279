""" Django reCAPTCHA Enterprise module.

This module provides a Django way to verify Google reCAPTCHA Enterprise

Usage:

    from gdmty_django_recaptcha_enterprise import assess_token
    ...
    # token is the token to verify and action is the name of the action to be verified
    if assess_token(token, action):
        # do something
        ...

"""

__title__ = "gdmty_django_recaptcha_enterprise"
__version__ = "24.5.3"
__description__ = "reCAPTCHA Enterprise's Django module for verifying reCAPTCHA tokens"
__url__ = "https://github.com/SIGAMty/gdmty-django-recaptcha-enterprise"
__author__ = "César Benjamín"
__author_email__ = "mathereall@gmail.com"
__license__ = "Apache 2.0"
__keywords__ = ["django", "recaptcha", "enterprise", "google"]
VERSION = __version__

