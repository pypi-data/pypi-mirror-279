# -*- coding: utf-8 -*-
from __future__ import annotations

import glob
import logging
import os
from pathlib import Path
import sys
import time

import dask
from dask.distributed import Client, LocalCluster, wait, system
from dask.distributed import progress as distributed_progress
import psutil

logger = logging.getLogger(__name__)


def progress(fs):
    """
    Perform outstanding calculations similar to :func:`distributed.progress`.

    Detects whether we are in an interactive environment or not. In an
    interactive environment we use :func:`distributed.progress` to output a
    dynamic progress bar during the calculations. In a non-interactive
    setting, we don't output anything and just :func:`distributed.wait` for the
    end of the calculations. This is useful to keep log files clean for HPC
    jobs.

    Parameters
    ----------
    fs : Future
    """
    if sys.stdout.isatty():
        return distributed_progress(fs)
    else:
        wait(fs)
        return fs


def cpu_count_physical() -> int | None:
    # Adapted from psutil
    """
    Return the number of physical cores in the system.

    Used to detect hyperthreading.

    Returns
    -------
    no_cores : int or None
        Number of physical cores or `None` if not detectable.
    """
    IDS = ["physical_package_id", "die_id", "core_id", "book_id", "drawer_id"]
    core_ids = set()
    for path in glob.glob("/sys/devices/system/cpu/cpu[0-9]*/topology"):
        core_id = []
        for id in IDS:
            id_path = os.path.join(path, id)
            if os.path.exists(id_path):
                with open(id_path) as f:
                    core_id.append(int(f.read()))
        core_ids.add(tuple(core_id))
    result = len(core_ids)
    if result != 0:
        return result
    else:
        return None


def hyperthreading_info() -> tuple[bool | None, int | None, int | None]:
    """
    Detect presence of hyperthreading.

    If there are more logical cpus than physical ones, hyperthreading is
    active.

    Returns
    -------
    hyperthreading : bool or None
        If `True`, hyperthreading is active
    no_logical_cpus : int or None
        Number of logical cpus
    no_physical_cpus : int or None
        Number of physical cpus
    """
    no_logical_cpus = psutil.cpu_count(logical=True)
    no_physical_cpus = cpu_count_physical()
    if no_logical_cpus is None or no_physical_cpus is None:
        hyperthreading = None
    else:
        hyperthreading = no_logical_cpus > no_physical_cpus
    return (hyperthreading, no_logical_cpus, no_physical_cpus)


def restart_cluster(client: Client) -> None:
    """
    Restarts cluster.

    Parameters
    ----------
    client : Scheduler
    """
    info = client.scheduler_info()

    def total_executing():
        return sum(sum(w) for w in client.processing().values())

    expected_nr_workers = len(info["workers"])
    retries = 5
    while (nr_executing := total_executing()) > 0:
        logger.info(f"Waiting for {nr_executing} tasks to finish")
        time.sleep(60)
        if retries > 0:
            logger.info(f"Retrying with {retries} retries left.")
            retries -= 1
        else:
            logger.info("Retries exhausted. Hoping for the best.")
            break
    client.restart()
    client.wait_for_workers(expected_nr_workers, 120)


class DummyClient:
    """
    Dummy class mimicking :class:`distributed.Client` without `distributed`.
    """

    def persist(self, x):
        return x


class DistributedLocalClusterScheduler:
    """
    Scheduler using :class:`distributed.LocalCluster` for local parallelism.

    Recommended way to use on a single machine.
    """

    def __init__(self, threads_per_worker=2, **kwargs) -> None:
        (hyperthreading, no_logical_cpus, no_physical_cpus) = hyperthreading_info()
        if hyperthreading:
            factor = no_logical_cpus // no_physical_cpus
            no_available_physical_cpus = dask.system.CPU_COUNT // factor
            n_workers = no_available_physical_cpus // threads_per_worker
            # leave one core for scheduler and client
            n_workers -= 1
            # but make sure to have at least one worker
            n_workers = max(1, n_workers)
            # use 90% of available memory for workers,
            # rest for scheduler, client, and system
            memory_limit = (system.MEMORY_LIMIT * 0.9) / n_workers
        else:
            # let dask figure it out
            n_workers = None
            memory_limit = None
        self.cluster = LocalCluster(
            n_workers=n_workers,
            threads_per_worker=threads_per_worker,
            memory_limit=memory_limit,
        )
        self.client = Client(self.cluster)

    def __enter__(self):
        self.cluster.__enter__()
        self.client.__enter__()
        return self

    def __exit__(self, type, value, traceback):
        self.client.__exit__(type, value, traceback)
        self.cluster.__exit__(type, value, traceback)


class ExternalScheduler:
    """
    Scheduler using an externally started :class:`distributed.Cluster`.

    This is useful if the cluster needs to be set up outside of the program,
    for example in a HPC environment or for debugging purposes.
    """

    def __init__(self, scheduler_file, auto_shutdown=True, **kwargs):
        p = Path(scheduler_file)
        time_to_wait = 10
        while not p.exists():
            time.sleep(1)
            time_to_wait -= 1
            if time_to_wait <= 0:
                raise RuntimeError("Scheduler does not exist")
        self.scheduler_file = scheduler_file
        self.client = Client(scheduler_file=scheduler_file)
        self.auto_shutdown = auto_shutdown

    def __enter__(self):
        self.client.__enter__()
        return self

    def __exit__(self, type, value, traceback):
        if self.auto_shutdown:
            self.client.shutdown()
        self.client.__exit__(type, value, traceback)


class LocalThreadsScheduler:
    """
    Scheduler using `dask` without `distributed`.

    Generally not useful due to the extensive use of
    :class:`distributed.Client` in the program. May occasionally be used for
    debugging.
    """

    def __init__(self, **kwargs):
        self.client = None

    def __enter__(self):
        dask.config.set(scheduler="threads")
        return self

    def __exit__(self, type, value, traceback):
        pass


class MPIScheduler:
    """
    Scheduler using dask.mpi for cluster setup.

    Should be avoided since the
    `Dask-MPI project <http://mpi.dask.org/en/latest>`_ seems to be
    out-of-date. For now, prefer :class:`ExternalScheduler`; might be revisited
    at a later time.
    """

    def __init__(self, **kwargs):
        from dask_mpi import initialize

        n_workers = 4  # tasks-per-node from scheduler
        n_threads = 4  # cpus-per-task from scheduler
        memory_limit = (system.MEMORY_LIMIT * 0.9) / n_workers
        initialize(
            "ib0",
            nthreads=n_threads,
            local_directory="/scratch/local",
            memory_limit=memory_limit,
        )
        self.client = Client()

    def __enter__(self):
        self.client.__enter__()
        return self

    def __exit__(self, type, value, traceback):
        self.client.__exit__(type, value, traceback)


class SingleThreadedScheduler:
    """
    Scheduler using strictly local, single threaded approach.

    Only for debugging.
    """

    def __init__(self, **kwargs):
        self.client = DummyClient()

    def __enter__(self):
        dask.config.set(scheduler="single-threaded")
        return self

    def __exit__(self, type, value, traceback):
        pass


#: Available schedulers. For detailed descriptions see the respective class.
SCHEDULERS = dict(
    [
        ("distributed-local-cluster", DistributedLocalClusterScheduler),
        ("external", ExternalScheduler),
        ("threaded", LocalThreadsScheduler),
        ("mpi", MPIScheduler),
        ("single-threaded", SingleThreadedScheduler),
    ]
)


def setup_scheduler(args):
    """
    Setup parallel environment, usually with a :class:`distributed.Client`.

    Parameters
    ----------
    args : argparse.Namespace
        Arguments to setup the scheduler. Generally, an entry from
        :const:`SCHEDULERS`.

    Returns
    -------
    scheduler : a scheduler
        One of the scheduler objects defined in :mod:`gordias.dask_setup`,
        suitable as a context manager.
    """
    scheduler_spec = args.dask_scheduler.split("@")
    scheduler_name = scheduler_spec[0]
    scheduler_kwargs = {k: v for k, v in (e.split("=") for e in scheduler_spec[1:])}
    scheduler = SCHEDULERS[scheduler_name]
    return scheduler(**scheduler_kwargs)
