import asyncio
from pathlib import Path

from playwright._impl._driver import compute_driver_executable, get_driver_env


async def open_trace_viewer(path: Path) -> int:
    driver_executable, driver_cli = compute_driver_executable()
    cmd = " ".join([driver_executable, driver_cli, "show-trace", str(path)])
    proc = await asyncio.create_subprocess_shell(
        cmd,
        env=get_driver_env(),
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    return proc.pid
