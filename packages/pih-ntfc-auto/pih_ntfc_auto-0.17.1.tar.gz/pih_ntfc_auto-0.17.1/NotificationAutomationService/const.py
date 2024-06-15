import ipih

from pih.consts.hosts import Hosts
from pih.collections.service import ServiceDescription

NAME: str = "NotificationAutomation"

HOST = Hosts.BACKUP_WORKER

VERSION: str = "0.17.1"

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Notification automation service",
    host=HOST.NAME,
    use_standalone=True,
    version=VERSION,
    standalone_name="ntfc_auto",
)
