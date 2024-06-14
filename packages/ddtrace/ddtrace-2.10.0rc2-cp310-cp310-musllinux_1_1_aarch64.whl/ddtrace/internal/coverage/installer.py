from pathlib import Path
import typing as t

from ddtrace.internal.coverage.code import ModuleCodeCollector
from ddtrace.internal.coverage.multiprocessing_coverage import _patch_multiprocessing
from ddtrace.internal.coverage.threading_coverage import _patch_threading


def install(include_paths: t.Optional[t.List[Path]] = None) -> None:
    ModuleCodeCollector.install(include_paths=include_paths)
    _patch_multiprocessing()
    _patch_threading()
