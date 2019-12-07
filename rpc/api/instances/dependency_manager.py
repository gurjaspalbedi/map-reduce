from dependency_injector import providers, containers
from .service_account import ServiceAccount
from .configurations import PreemtibleMachine


class Dependencies(containers.DeclarativeContainer):
    service_account = providers.Singleton(ServiceAccount)
    preem_machine = providers.Singleton(PreemtibleMachine)
