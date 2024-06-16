import os

import ipih

from pih import A
from BackupService.api import *
from BackupService.const import *
from pih.collections import Result, RobocopyJobStatus
from pih.tools import ParameterList, e, n, nn, ne, nns, jnl, esc, escs


from datetime import datetime
from typing import Any
import grpc


import json

SC = A.CT_SC

ISOLATED: bool = False


class DH:
    job_config_file_path: str = ""


def start(as_standalone: bool = False) -> None:

    def load_job_config_file() -> None:
        DH.job_config_file_path = (
            nns(A.SE.named_arg(JOB_CONFIG_ALIAS))
            or "//fmv.lan/facade/.files/backup/job_config.json"
        )
        work_directory: str = os.path.dirname(os.path.realpath(__file__))

        job_config_file_default_path: str = A.PTH.join(
            work_directory, PATH.JOB_CONFIG.FILE_NAME
        )
        DH.job_config_file_path = (
            DH.job_config_file_path or job_config_file_default_path
        )
        if not A.PTH.exists(DH.job_config_file_path) and A.PTH.exists(
            job_config_file_default_path
        ):
            DH.job_config_file_path = job_config_file_default_path
            A.O.error("Config job file not found")
            A.O.value("Used default config job file", job_config_file_default_path)
        else:
            if n(DH.job_config_file_path):
                A.O.value(
                    jnl(
                        (
                            j(("Argument ", esc(JOB_CONFIG_ALIAS), " is not set.")),
                            "Use default job config path",
                        )
                    ),
                    job_config_file_default_path,
                )
        if A.PTH.exists(DH.job_config_file_path):
            data: dict = json.load(open(DH.job_config_file_path))
            PATH.JOB_CONFIG.DIRECTORY_NAME = data["job_config_directory"]
            PATH.JOB_CONFIG.DIRECTORY = A.PTH.join(
                A.PTH.get_file_directory(DH.job_config_file_path),
                PATH.JOB_CONFIG.DIRECTORY_NAME,
            )
            ROBOCOPY.JOB_MAP = data["job_config_map"]
        else:
            A.O.error("Config job file not found")
            A.SE.exit(0)

    A.SE.add_isolated_arg()
    A.SE.add_arg(JOB_CONFIG_ALIAS, nargs="?", const="True", type=str)

    def robocopy_job_handler(
        name: str | None,
        source: str | None,
        destination: str | None,
        force: bool = False,
    ) -> bool:
        rjl: list[RobocopyJobItem] = BackupApi.get_job_list()
        rjl = rjl if e(name) else A.D.filter(lambda item: item.name == name, rjl)
        rjl = rjl if e(source) else A.D.filter(lambda item: item.source == source, rjl)
        rjl = (
            rjl
            if e(destination)
            else A.D.filter(lambda item: item.destination == destination, rjl)
        )
        for job_item in rjl:
            BackupApi().start_robocopy_job(job_item, force)
        return len(rjl) > 0

    def heat_beat_action(current_datetime: datetime) -> None:
        if nn(ROBOCOPY.JOB_MAP):
            rjl: list[RobocopyJobItem] = BackupApi.get_job_list()
            for rji in rjl:
                if ne(rji.start_cron_string) and A.D_C.now(
                    nns(rji.start_cron_string), current_datetime
                ):
                    BackupApi().start_robocopy_job(rji)

    def service_call_handler(sc: SC, pl: ParameterList, context) -> Any:
        if sc == SC.heart_beat:
            heat_beat_action(A.D_Ex.parameter_list(pl).get())
            return True
        if sc == SC.robocopy_start_job:
            if robocopy_job_handler(
                pl.next(),
                pl.next(),
                pl.next(),
                pl.next(),
            ):
                return True
            return A.ER.rpc(
                context,
                j(("Robocopy job: ", escs(pl.values[0:3]))),
                grpc.StatusCode.NOT_FOUND,
            )
        if sc == SC.robocopy_get_job_status_list:
            rjl: list[RobocopyJobItem] = BackupApi.get_job_list()
            result: list[RobocopyJobStatus] = []
            for job_item in rjl:
                rjs: RobocopyJobStatus = BackupApi.get_job_status(
                    nns(job_item.name), nns(job_item.source), nns(job_item.destination)
                )
                rjs.exclude = job_item.exclude
                result.append(rjs)
            return Result(None, result)

    def service_starts_handler() -> None:
        A.SRV_A.subscribe_on(SC.heart_beat)

    A.O.init()
    load_job_config_file()

    A.SRV_A.serve(
        SD,
        service_call_handler,
        service_starts_handler,
        isolate=ISOLATED,
        as_standalone=as_standalone,
    )


if __name__ == "__main__":
    start()
