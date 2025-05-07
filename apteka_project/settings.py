# apteka_project/settings.py

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# Бул сап settings.py файлынан эки деңгээл жогору турган негизги долбоор папкасын көрсөтөт.
# (manage.py файлы жайгашкан жер)
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# ӨЗҮҢҮЗДҮН УНИКАЛДУУ SECRET_KEY'ИҢИЗДИ БУЛ ЖЕРГЕ КОЮҢУЗ!
# Ар бир жаңы долбоордо бул автоматтык түрдө генерацияланат.
SECRET_KEY = 'django-insecure-бул_жерге_сиздин_уникалдуу_жана_коопсуз_ачкычыңыз_коюлат!' # ӨЗГӨРТҮҢҮЗ!

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True # Иштеп чыгуу учурунда True, продакшенде False болот

ALLOWED_HOSTS = ['127.0.0.1', 'localhost'] # DEBUG=False болгондо бул жерге домен атыңызды кошосуз

# Application definition

INSTALLED_APPS = [
    # 'jazzmin', # Эгер Django Jazzmin колдонсоңуз, admin'ден мурун турушу керек
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', # Статикалык файлдарды тейлөө үчүн
    'rest_framework', # API үчүн
    'corsheaders',    # CORS үчүн (эгер фронтенд башка доменде болсо)
    'api.apps.ApiConfig', # Сиздин 'api' тиркемеңиз
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', # CORS үчүн, CommonMiddleware'ден мурун
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'apteka_project.urls' # Негизги urls.py файлын көрсөтөт

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # Негизги 'templates' папкасын көрсөтөт
        'APP_DIRS': True, # Тиркемелердин ичиндеги 'templates' папкаларын да издөө
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request', # Шаблондордо 'request' объектисин колдонуу үчүн
                'django.contrib.auth.context_processors.auth', # Шаблондордо 'user' объектисин колдонуу үчүн
                'django.contrib.messages.context_processors.messages', # Шаблондордо билдирүүлөрдү көрсөтүү үчүн
            ],
        },
    },
]

WSGI_APPLICATION = 'apteka_project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internationalization
LANGUAGE_CODE = 'ky-KG' # Сайттын негизги тили (Кыргызча)
TIME_ZONE = 'Asia/Bishkek' # Сиздин убакыт алкагыңыз
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images for site design)
STATIC_URL = '/static/' # Статикалык файлдарга кайрылуу үчүн URL префикси

# Django'го статикалык файлдарды кайдан издөө керектигин көрсөтөт (DEBUG=True учурунда)
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# `collectstatic` буйругу үчүн (продакшенде статикалык файлдарды чогултуучу жер)
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles_prod') # Азырынча бул кереги жок

# Media files (User uploaded files like images for medicines)
MEDIA_URL = '/media/' # Медиа файлдарга кайрылуу үчүн URL префикси
MEDIA_ROOT = os.path.join(BASE_DIR, 'media') # Медиа файлдар сактала турган негизги 'media' папкасы

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication URLs (Кирүү/Чыгуу багыттары)
LOGIN_REDIRECT_URL = '/'  # Ийгиликтүү киргенден кийин башкы бетке
LOGOUT_REDIRECT_URL = '/' # Ийгиликтүү чыккандан кийин башкы бетке
LOGIN_URL = 'login'       # `{% url 'login' %}` иштеши үчүн (эгер `accounts/` колдонсоңуз)

# CORS (эгер керек болсо)
CORS_ALLOWED_ORIGINS = [
    # "http://localhost:3000", # Фронтенддин дареги (мисал)
    # "http://127.0.0.1:3000",
]
# CORS_ALLOW_ALL_ORIGINS = True # Иштеп чыгуу үчүн (этият болуңуз)