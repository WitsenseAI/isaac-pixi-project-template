"""Check that Isaac Sim, Isaac Lab and CUDA PyTorch load on this machine.

pixi run check
"""

import importlib
import sys
from importlib.metadata import version

from isaacsim import SimulationApp

PACKAGES = ("isaacsim", "isaaclab", "torch")
WARMUP_FRAMES = 10


def report_versions() -> None:
    for package in PACKAGES:
        print(f"{package} {version(package)}")


def report_cuda() -> bool:
    torch = importlib.import_module("torch")
    if not torch.cuda.is_available():
        print("CUDA: not available")
        return False
    print(f"CUDA: {torch.cuda.get_device_name(0)}")
    return True


def main() -> int:
    simulation_app = SimulationApp({"headless": True})
    # Isaac Lab's simulation modules need the Kit app that SimulationApp starts.
    importlib.import_module("isaaclab.sim")
    for _ in range(WARMUP_FRAMES):
        simulation_app.update()
    report_versions()
    cuda_ok = report_cuda()
    simulation_app.close()
    return 0 if cuda_ok else 1


if __name__ == "__main__":
    sys.exit(main())
