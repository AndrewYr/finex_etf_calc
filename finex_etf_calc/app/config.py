import os

from finex_etf_calc.app.utils import MagConfig

ENVIRONMENT = os.environ['ENVIRONMENT'].upper()
CONFIG_FILE = os.environ.get('CONFIG_FILE',
                             f'{os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))}/config/{ENVIRONMENT.lower()}.yml')

README_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    'README.md',
)


class Environment:
    LOCAL = 'LOCAL'
    TESTING = 'TESTING'


class BaseConfig(MagConfig):
    ENVIRONMENT: str
    APP_NAME: str

    @property
    def ENVIRONMENT(self):
        return str(ENVIRONMENT).upper()

    README_PATH = README_PATH
    DB_PG_NAME: str
    DB_PG_USERNAME: str
    DB_PG_PASSWORD: str
    DB_PG_HOST: str
    DB_PG_PORT: int = 5432

    DB_SCHEMA: str
    DB_NAME: str

    FINEX_PRICE_ON_DAY_URL: str
    FINEX_PRICE_HISTORY_URL: str
    CBR_URL: str

    RABBITMQ_URLS: list

    @property
    def CELERY_URLS(self):
        return [f'{url.rstrip("/")}' for url in self.RABBITMQ_URLS]

    @property
    def ASYNC_DB_URL(self):
        return '{drivername}://{user}:{password}@{host}:{port}/{database}'.format(
            drivername='postgresql+asyncpg',
            user=self.DB_PG_USERNAME,
            password=self.DB_PG_PASSWORD,
            host=self.DB_PG_HOST,
            port=self.DB_PG_PORT,
            database=self.DB_PG_NAME,
        )

    @property
    def ALEMBIC_CONFIG(self):
        return '{drivername}://{user}:{password}@{host}:{port}/{database}'.format(
            drivername='postgresql+psycopg2',
            user=self.DB_PG_USERNAME,
            password=self.DB_PG_PASSWORD,
            host=self.DB_PG_HOST,
            port=self.DB_PG_PORT,
            database=self.DB_PG_NAME,
        )


class TestingConfig(BaseConfig):
    """Для запуска юнит тестов"""
    INIT_LOGGING: bool = False
    TESTING: bool = True
    DEBUG: bool = True


class LocalConfig(BaseConfig):
    pass


config_class = {
    Environment.LOCAL: LocalConfig,
    Environment.TESTING: TestingConfig,
}.get(ENVIRONMENT.upper(), BaseConfig)


config: BaseConfig = config_class.from_file(CONFIG_FILE)
