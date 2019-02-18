from locadora.settings.common import *
import re
import django_heroku

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECRET_KEY = 'pr1c7f_vn81cmvo+zlcmt)9jmtwx@p_l^@wga+l#(%3&h6mrcs'

#Segurança
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

ADMINS = [
    ('Woshington Valdeci de Sousa', 'wvs2@cin.ufpe.br'),
    ('Rennan Francisco Messias de Lima', 'mrennan.lima@gmail.com')
]

MANAGERS = [
    ('Woshington Valdeci de Sousa', 'wvs2@cin.ufpe.br'),
    ('Rennan Francisco Messias de Lima', 'mrennan.lima@gmail.com')
]

#Error Reporting
IGNORABLE_404_URLS = [
    re.compile(r'^/apple-touch-icon.*\.png$'),
    re.compile(r'^/favicon\.ico$'),
    re.compile(r'^/robots\.txt$'),
]

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'locadora_db',
        'USER': 'mprof2018',
        'PASSWORD': 'mprof2018',
        'HOST': 'http://127.0.0.1',
    }
}




STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

django_heroku.settings(locals())
