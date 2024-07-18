import logging
import os

from celery.schedules import crontab
from flask_appbuilder.security.manager import AUTH_OAUTH
from flask_caching.backends.filesystemcache import FileSystemCache
from superset.security import SupersetSecurityManager

# ================================================================================================================
# ================================================================================================================
# ================================================================================================================

logger = logging.getLogger()

DATABASE_DIALECT = os.getenv("DATABASE_DIALECT")
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_DB = os.getenv("DATABASE_DB")

EXAMPLES_USER = os.getenv("EXAMPLES_USER")
EXAMPLES_PASSWORD = os.getenv("EXAMPLES_PASSWORD")
EXAMPLES_HOST = os.getenv("EXAMPLES_HOST")
EXAMPLES_PORT = os.getenv("EXAMPLES_PORT")
EXAMPLES_DB = os.getenv("EXAMPLES_DB")

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = (
    f"{DATABASE_DIALECT}://"
    f"{DATABASE_USER}:{DATABASE_PASSWORD}@"
    f"{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_DB}"
)

SQLALCHEMY_EXAMPLES_URI = (
    f"{DATABASE_DIALECT}://"
    f"{EXAMPLES_USER}:{EXAMPLES_PASSWORD}@"
    f"{EXAMPLES_HOST}:{EXAMPLES_PORT}/{EXAMPLES_DB}"
)

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_CELERY_DB = os.getenv("REDIS_CELERY_DB", "0")
REDIS_RESULTS_DB = os.getenv("REDIS_RESULTS_DB", "1")

RESULTS_BACKEND = FileSystemCache("/app/superset_home/sqllab")

CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": REDIS_RESULTS_DB,
}
DATA_CACHE_CONFIG = CACHE_CONFIG

# ================================================================================================================
# ================================================================================================================
# ================================================================================================================

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
OAUTH_PROVIDER_URL = os.getenv("OAUTH_PROVIDER_URL")

AUTH_TYPE = AUTH_OAUTH
OAUTH_PROVIDERS = [
    {
        'name': 'Auth0',
        'token_key': 'access_token',
        'icon': 'fa-openid',
        'remote_app': {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'scope': 'openid profile email',
            'api_base_url': OAUTH_PROVIDER_URL,
            'server_metadata_url': f"{OAUTH_PROVIDER_URL}/.well-known/openid-configuration"
        }
    }
]


class Oauth2SecurityManager(SupersetSecurityManager):
    def oauth_user_info(self, provider, response=None):
        response = self.appbuilder.sm.oauth_remotes[provider].get('userinfo')
        me = response.json()
        logger.info("JSON: {0}".format(me))
        return {
            'name': me['name'],
            'email': me['email'],
            'id': me['sub'],
            'username': me['name'],
            'first_name': '',
            'last_name': '',
            'is_active': True
        }


CUSTOM_SECURITY_MANAGER = Oauth2SecurityManager
AUTH_USER_REGISTRATION = True
AUTH_ROLES_SYNC_AT_LOGIN = True
AUTH_USER_REGISTRATION_ROLE = "Admin"


# ================================================================================================================
# ================================================================================================================
# ================================================================================================================

class CeleryConfig:
    broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
    imports = ("superset.sql_lab",)
    result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}"
    worker_prefetch_multiplier = 1
    task_acks_late = False
    beat_schedule = {
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=10, hour=0),
        },
    }


CELERY_CONFIG = CeleryConfig

# ================================================================================================================
# ================================================================================================================
# ================================================================================================================

FEATURE_FLAGS = {"ALERT_REPORTS": True}
ALERT_REPORTS_NOTIFICATION_DRY_RUN = True
WEBDRIVER_BASEURL = "http://superset:8088/"  # When using docker compose baseurl should be http://superset_app:8088/
# The base URL for the email report hyperlinks.
WEBDRIVER_BASEURL_USER_FRIENDLY = WEBDRIVER_BASEURL
SQLLAB_CTAS_NO_LIMIT = True

try:
    import superset_config_docker
    from superset_config_docker import *  # noqa

    logger.info(f"Loaded your Docker configuration at " f"[{superset_config_docker.__file__}]")
except ImportError:
    logger.info("Using default Docker config...")
