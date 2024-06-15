import ipih

from pih import A
from pih.collections import RobocopyJobDescription
from pih.collections.service import ServiceDescription

NAME: str = "Backup"

VERSION: str = "0.17.2"


JOB_CONFIG_ALIAS: str = "job_config"


class ROBOCOPY:

    NAME: str = "robocopy"
    JOB_PARAMETER_NAME: str = "/job:"

    JOB_MAP: dict[str, dict[str, list[RobocopyJobDescription]]] | None = None



HOST = A.CT_H.BACKUP_WORKER

STANDALONE_NAME: str = "backup"

class PATH:

    class JOB_CONFIG:

        FILE_NAME: str = A.PTH.add_extension(JOB_CONFIG_ALIAS, A.CT_F_E.JSON)
        DIRECTORY_NAME: str = "robocopy_config"
        DIRECTORY_PATH: str = A.PTH.join(
            A.PTH.FACADE.SERVICE(NAME),
            DIRECTORY_NAME,
        )

        VALUE: str = A.PTH.join(A.PTH.FACADE.SERVICE_FILES(STANDALONE_NAME), FILE_NAME)


SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Backup service",
    host=HOST.NAME,
    commands=("robocopy_start_job", "robocopy_get_job_status_list"),
    version=VERSION,
    standalone_name=STANDALONE_NAME,
    use_standalone=True,
    parameters={JOB_CONFIG_ALIAS: PATH.JOB_CONFIG.VALUE},
)
