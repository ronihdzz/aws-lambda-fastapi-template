from loguru import logger

from core.settings import settings
from db.posgresql.models.public import (  # import all models for create tables for database testing
    Book
)
from shared.environment import AppEnvironment
from tests.create_databases import prepare_database

if settings.ENVIRONMENT in [AppEnvironment.TESTING, AppEnvironment.TESTING_DOCKER]:
    logger.info("Preparing database for tests")
    prepare_database(
        schemas_to_create=["public"],
    )