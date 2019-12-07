from dependency_injector import providers, containers
from .log.logger import DataStoreLogger

class Dependencies(containers.DeclarativeContainer):
    log = providers.Singleton(DataStoreLogger)