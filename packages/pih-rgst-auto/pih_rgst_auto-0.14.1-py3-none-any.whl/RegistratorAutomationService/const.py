import ipih

from pih import A, package_name
from pih.collections.service import ServiceDescription


NAME: str = "RegistratorAutomation"

HOST = A.CT_H.BACKUP_WORKER


PACKAGES: tuple[str, ...] = (
    package_name(A.CT_SR.MOBILE_HELPER),  # type: ignore
)

VERSION: str = "0.14.1"

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Registrator Automation service",
    host=HOST.NAME,
    version=VERSION,
    standalone_name="rgst_auto",
    use_standalone=True,
    packages=PACKAGES,
)
