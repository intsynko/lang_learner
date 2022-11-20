from ..base import env

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": env.db("DATABASE_URL", "postgres://postgres:postgres@localhost:5432/postgres", "postgres")
}
