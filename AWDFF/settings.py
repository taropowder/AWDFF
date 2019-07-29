"""
Django settings for AWDFF project.

Generated by 'django-admin startproject' using Django 2.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import time
import yaml

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zj+ej_($gs6j%2tp5%d2_!_sh%vm5o_)8j1r(lno!1%vn$dkbn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'problem',
    'competition',
    'account',
    'team',
    'django_crontab',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AWDFF.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'admin_tools.template_loaders.Loader',
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
        },
    }, ]
# TEMPLATES_LOADERS = (
#     "admin_tools.template_loaders.Loader",
# )

WSGI_APPLICATION = 'AWDFF.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'
#
# TIME_ZONE = 'UTC'

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
AUTH_USER_MODEL = 'account.Member'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

ADMIN_TOOLS_MENU = 'menu.CustomMenu'
ADMIN_TOOLS_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'dashboard.CustomAppIndexDashboard'

# * 0/1 * * * ?   echo 'test' >> /tmp/test.txt
# 后面的>> /tmp/testapi_crontab.log' 表示将定时执行的函数的打印结果输出到已经在本机中建立好的log文件中，方便调试。
CONFIG_YML = os.path.join(BASE_DIR, 'config.yml')

if not os.path.exists(CONFIG_YML):
    print('there is no config.yml, please check are you init')
    exit()


with open(CONFIG_YML, 'r') as f:
    config = yaml.safe_load(f.read())
    START_TIME = config['start_time']
    END_TIME = config['end_time']
    # check时间
    CHECK_TIME_INTERVAL = config['check_time_interval']
    # 每轮持续时间
    ROUND_TIME_INTERVAL = config['round_time_interval']
    CHECK_LOG = config['check_log']
    ROUND_LOG = config['round_log']
    PLAY_NOW = config['play_now']
if not PLAY_NOW:
    _start_time = time.strptime(START_TIME, "%Y/%m/%d %H:%M:%S")
    _end_time = time.strptime(END_TIME, "%Y/%m/%d %H:%M:%S")

    CRON_TEMPLATE = '*/{times} {start_hour}-{end_hour} {start_day}-{end_day} {month} *'

    CHECKER_CRON = CRON_TEMPLATE.format(times=CHECK_TIME_INTERVAL, start_hour=_start_time.tm_hour,
                                        end_hour=_end_time.tm_hour
                                        , start_day=_start_time.tm_mday, end_day=_end_time.tm_mday,
                                        month=_start_time.tm_mon)

    ROUND_CRON = CRON_TEMPLATE.format(times=ROUND_TIME_INTERVAL, start_hour=_start_time.tm_hour,
                                      end_hour=_end_time.tm_hour
                                      , start_day=_start_time.tm_mday, end_day=_end_time.tm_mday,
                                      month=_start_time.tm_mon)
else:
    CRON_TEMPLATE = '*/{times} * * * *'
    CHECKER_CRON = CRON_TEMPLATE.format(times=CHECK_TIME_INTERVAL)
    ROUND_CRON = CRON_TEMPLATE.format(times=ROUND_TIME_INTERVAL)

CRONJOBS = [
    # 表示两分钟check一次
    (CHECKER_CRON, 'checker.start.check', f'>> {CHECK_LOG}'),
    # 十分钟刷新一轮
    (ROUND_CRON, 'refresh.refresh.refresh_flag', f'>> {ROUND_LOG}')
]
