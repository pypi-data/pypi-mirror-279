from contextlib import suppress
from itertools import cycle
from os import _exit as force_exit
from typing import cast

from psutil import pid_exists
from pymem import Pymem
from pymem.exception import ProcessNotFound
from win32api import MessageBox
from win32con import MB_ICONERROR, MB_OK

from trainerbase.config import pymem_config


def attach_to_process() -> Pymem:
    process_names = pymem_config["process_names"]

    if not process_names:
        raise ValueError("Empty process name list")

    print("Waiting for process in:", process_names)

    with suppress(KeyboardInterrupt):
        for process_name in cycle(process_names):
            try:
                pm = Pymem(
                    process_name,
                    exact_match=pymem_config["exact_match"],
                    ignore_case=pymem_config["ignore_case"],
                )
            except ProcessNotFound:
                continue

            print(f"Found {process_name}, pid: {pm.process_id}")

            return pm

    force_exit(0)


def show_message_and_shutdown_if_process_exited():
    if pid_exists(cast(int, _pm.process_id)):
        return

    MessageBox(
        None,
        "Shut down trainer?",
        "Process Exited!",
        MB_ICONERROR | MB_OK,
    )

    force_exit(0)


_pm = attach_to_process()
