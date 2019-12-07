from dependency_injector import providers, containers
from .log.logger import WorkerLogger

class Dependencies(containers.DeclarativeContainer):
    log = providers.Singleton(WorkerLogger)