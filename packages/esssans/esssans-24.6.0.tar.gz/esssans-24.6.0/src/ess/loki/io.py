# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2023 Scipp contributors (https://github.com/scipp)
"""
Loading and merging of LoKI data.
"""
import scipp as sc
from ess.reduce import nexus

from ess.sans.types import (
    Filename,
    LoadedNeXusDetector,
    LoadedNeXusMonitor,
    MonitorType,
    NeXusDetectorName,
    NeXusMonitorName,
    RawSample,
    RawSource,
    RunType,
)


def load_nexus_sample(file_path: Filename[RunType]) -> RawSample[RunType]:
    return RawSample[RunType](nexus.load_sample(file_path))


def dummy_load_sample(file_path: Filename[RunType]) -> RawSample[RunType]:
    return RawSample[RunType](
        sc.DataGroup({'position': sc.vector(value=[0, 0, 0], unit='m')})
    )


def load_nexus_source(file_path: Filename[RunType]) -> RawSource[RunType]:
    return RawSource[RunType](nexus.load_source(file_path))


def load_nexus_detector(
    file_path: Filename[RunType], detector_name: NeXusDetectorName
) -> LoadedNeXusDetector[RunType]:
    return LoadedNeXusDetector[RunType](
        nexus.load_detector(file_path=file_path, detector_name=detector_name)
    )


def load_nexus_monitor(
    file_path: Filename[RunType],
    monitor_name: NeXusMonitorName[MonitorType],
) -> LoadedNeXusMonitor[RunType, MonitorType]:
    return LoadedNeXusMonitor[RunType, MonitorType](
        nexus.load_monitor(file_path=file_path, monitor_name=monitor_name)
    )


providers = (
    load_nexus_detector,
    load_nexus_monitor,
    load_nexus_sample,
    load_nexus_source,
)
"""Providers for loading single files."""
