from .base import *
import MyImportantInfo as MIF

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = MIF.DJANGO_SECRET_KEY()

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


try:
    from .local import *
except ImportError:
    pass
