from settings.base import env

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': env.str('REDIS_CACHE', default='redis://127.0.0.1:6379/0'),
    },
    'repeats': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': env.str('REDIS_CACHE', default='redis://127.0.0.1:6379/1'),
    },
    'file_uploading': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': env.str('REDIS_CACHE', default='redis://127.0.0.1:6379/2'),
    }
}

MAIN_PAGE_CACHE_TIMEOUT = 3600