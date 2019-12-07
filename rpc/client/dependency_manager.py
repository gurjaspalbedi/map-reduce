from dependency_injector import providers, containers
from logger import ClientLogger

class Dependencies(containers.DeclarativeContainer):
    log = providers.Singleton(ClientLogger)