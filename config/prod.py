from . import settings
from .settings import *

DEBUG = False
ALLOWED_HOSTS = settings.ALLOWED_HOSTS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': secrets['DB_SETTINGS']["default"]["NAME"],
        'USER': secrets['DB_SETTINGS']["default"]["USER"],
        'PASSWORD': secrets['DB_SETTINGS']["default"]["PASSWORD"],
        'HOST': secrets['DB_SETTINGS']["default"]["HOST"],
        'PORT': secrets['DB_SETTINGS']["default"]["PORT"],
    }
}
